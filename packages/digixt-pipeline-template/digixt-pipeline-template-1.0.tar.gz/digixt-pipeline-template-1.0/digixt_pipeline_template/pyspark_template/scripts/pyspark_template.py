from pyspark.sql.functions import *
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote
import copy
from pyspark.sql.types import StructType
from pyspark.sql.functions import lit

# Custom Dependencies
# TODO: this is added to help airflow detect common_utils as module
import sys
import os
sys.path.append("/workflows/pyspark_template/")
# sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
# print("path : {}".format(os.path.dirname(__file__) + '/../'))

from common_utils.scripts.common_utilities import CommonLogging, CommonIcebergUtilities
from common_utils.scripts.helper.common_helper_utilities import CommonProcessHelperUtils, CommonAPIUtilities
from common_utils.scripts.data.common_data_utilities import CommonDataUtilities
from common_utils.scripts.s3.common_s3_utilities import CommonS3Utilities


logging = CommonLogging.get_logger()

# ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****

MOUNT_BUCKET = '/workflows'

class DefaultSparkCode:
    def get_dummy_data():
        data = [
            {
                "full_name":"John Smith",
                "dob":  "1980-02-09",
                "position": "Senior  Data Engineer",
                 "salary": 30000.00
            },
            {
                "full_name":"Hana Peter",
                "dob":  "1984-12-29",
                "position": "Software Engineer",
                 "salary": 25000.00
            },
            {
                "full_name":"Ali Abdela",
               "dob":  "1985-08-19",
                "position": "Data Engineer",
                 "salary": 28000.00
            }
        ]
        return data
    
   

    def ingest_data(s3_schema_file_path, schema_file_object_key,output_wh_table_load_strategy, 
                output_warehouse_fq_table, output_table_snapshots_delete_period):

        minio_s3_source = CommonS3Utilities.MinioS3Resource(minio_s3_credentials).minio_s3_resource

        config_table_schema = CommonProcessHelperUtils.get_schema_from_s3(s3_schema_file_path, schema_file_object_key, minio_s3_source)
        # config_table_schema =   CommonProcessHelperUtils.get_schema_from_local(s3_schema_file_path, schema_file_object_key)
        # get dummy data                                                             
        input_records_list =  DefaultSparkCode.get_dummy_data()     

        logging.info("config_spark_schema_json:" + str(config_table_schema))
        logging.info(f"Length of input_records_list:{str(len(input_records_list))}")

        data_rdd = sc.parallelize(input_records_list)

        format_data_rdd = data_rdd.map(lambda x: CommonDataUtilities.format_data(x, config_table_schema))

        spark_schema_json = CommonDataUtilities.create_spark_schema(config_table_schema)

        logging.info("spark_schema_json:" + str(spark_schema_json))
        data_df = spark.createDataFrame(format_data_rdd, schema=StructType.fromJson(spark_schema_json))

        # Adding this to remove duplicates, we may get duplicates
        data_df = data_df.drop_duplicates()

        data_df = data_df.withColumn("ingested_at", to_timestamp(lit(current_timestamp())))

        script_adding_columns = ["ingested_at"]
        logging.info(">> Dataframe schema: " + str(data_df.schema))
        logging.info(">> Dataframe spark_schema_json: " + str(spark_schema_json))
        logging.info(">> Display 10 rows: " + str(spark_schema_json))

        data_df.show(10, truncate=False)

        CommonIcebergUtilities.iceberg_load_operation(spark, output_wh_table_load_strategy, data_df,
                                                    output_warehouse_fq_table, script_adding_columns,
                                                    merge_data_join_fields=None)

        warehouse_catalog, warehouse_schema, warehouse_ref_table = output_warehouse_fq_table.split(".")

        # ********************************************************
        # Drop the data by ingested_at  -
        # Maintain only one snapshot in one week.
        # Maintain last 3 months data snapshots
        data_df.printSchema()
        # delete_sql_query = """
        #     DELETE FROM {} WHERE 
        #     (ingested_at < date_sub(CURRENT_TIMESTAMP(), {})) 
        #     OR (
        #             (ingested_at <> (SELECT max(ingested_at) FROM  {})) 
        #             AND 
        #             (ingested_at > date_sub(CURRENT_TIMESTAMP(), 6))
        #         )
        # """.format(output_warehouse_fq_table, output_table_snapshots_delete_period, output_warehouse_fq_table)

        # logging.info(f"Clear History snapshots, delete_sql_query:{delete_sql_query}")
        # spark.sql(delete_sql_query)
        # ********************************************************
        CommonIcebergUtilities.optimize_commands(spark, warehouse_catalog, warehouse_schema, warehouse_ref_table)
                                                             
    

def main():
    try:
        task_name = spark_job_args["task_name"]
        s3_schema_file_path = spark_job_args["s3_schema_file_path"]
        schema_file_object_key = spark_job_args["schema_file_object_key"]
        project_dir_name = spark_job_args["project_dir_name"]

        logging.info("""task_name: %s, s3_schema_file_path: %s, schema_file_object_key: %s
                """.format(task_name, s3_schema_file_path, schema_file_object_key))
        # Arguments - DW output table
        output_warehouse_fq_table = spark_job_args["output_warehouse_fq_table"]
        output_wh_table_load_strategy = spark_job_args["output_wh_table_load_strategy"]
        output_table_snapshots_delete_period = spark_job_args.get("output_table_snapshots_delete_period", 60)
        logging.info("""output_warehouse_fq_table: %s, output_wh_table_load_strategy: %s, output_table_snapshots_delete_period: %s
                """.format(output_warehouse_fq_table, output_wh_table_load_strategy, output_table_snapshots_delete_period))

        # Starter spark code  called
        DefaultSparkCode.ingest_data(s3_schema_file_path, schema_file_object_key,output_wh_table_load_strategy, 
                output_warehouse_fq_table, output_table_snapshots_delete_period)

      
    except Exception as ex:
        logging.error(ex)
        sc.stop()
        raise Exception('! Something went wrong with this job')

    finally:
        logging.info('Stopping...')
        sc.stop()


if __name__ == '__main__':
    # Provide Spark Session additional config options as dictionary
    spark_options = {
        "spark.sql.shuffle.partitions": "10",
        "spark.default.parallelism": "10"
    }
    spark, sc, spark_app_name, spark_job_args, cluster_details_spark_args, minio_s3_credentials,\
    credentials, *_ret_list = CommonProcessHelperUtils.initialize_read_arguments(spark_options=spark_options, mount_bucket_name=MOUNT_BUCKET)
    logging.info(f"spark_job_args: {spark_job_args}")
   

    main()
    exit()

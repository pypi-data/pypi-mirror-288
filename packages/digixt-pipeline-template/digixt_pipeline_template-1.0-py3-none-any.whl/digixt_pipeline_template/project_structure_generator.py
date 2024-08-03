import argparse
import os
import shutil
import json

class Constants:
    RENAMING_ALLOWED_DIRECTORIES = ['flows', 'config', 'scripts']
    DEAULT_TEMPLATE_DIR_NAME = 'pyspark_template'
    DEAULT_TEMPLATE_DATA_SCHEMA_FILE_NAME = 'employee_data_schema'


class CommonLogging:
    @staticmethod
    def get_logger(log_level_str='INFO'):
        import logging
        try:
            level_num = logging.getLevelName(log_level_str.upper())
            if not isinstance(level_num, int):
                raise ValueError(f"Logging Level is not in predefined list: {str(level_num)}")

        except ValueError:
            level_num = logging.getLevelName('INFO')

        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=level_num,
                            datefmt='%y/%m/%d %H:%M:%S')

        return logging.getLogger()


logging = CommonLogging.get_logger()

class ProjectStructureGenerator:
    @staticmethod
    def copy_and_rename_template(project_name):
        # Define paths
        template_dir = os.path.join(os.path.dirname(__file__), Constants.DEAULT_TEMPLATE_DIR_NAME)
        current_dir = os.getcwd()
        logging.info("current_dir: {}".format(current_dir))
        # Copy template directory to current directory
        try:
            shutil.copytree(template_dir, os.path.join(current_dir, project_name))
            logging.debug(f"Copying template directory from {template_dir} to {os.path.join(current_dir, project_name)}")
             # Log creation of first-level directories
            destination_dir = os.path.join(current_dir, project_name)
            for dirpath, _, _ in os.walk(destination_dir):
                if dirpath == destination_dir:
                    continue
                logging.info(f"Creating directory: {os.path.relpath(dirpath, destination_dir)}")

        except FileExistsError:
            logging.error(f"Error: Directory '{project_name}' already exists. Aborting.")
            return
        except Exception as e:
                raise Exception(f"Error occurred while copying template: {str(e)}")
        
        # List of directories where renaming is allowed
        for dir in Constants.RENAMING_ALLOWED_DIRECTORIES:
            dir_path = os.path.join(current_dir,project_name,  dir)
            if os.path.exists(dir_path):
                for filename in os.listdir(dir_path):
                    name, ext = os.path.splitext(filename)
                    if name in [Constants.DEAULT_TEMPLATE_DIR_NAME, Constants.DEAULT_TEMPLATE_DATA_SCHEMA_FILE_NAME] and ext != '':
                        # Determine new filename with the project_name preserved extension
                        new_filename = project_name + ext
                        if name.endswith("_schema") and ext == ".json":
                            new_filename = project_name.replace('-', '_') + "_schema.json"

                        original_file_path = os.path.join(dir_path, filename)
                        new_file_path = os.path.join(dir_path, new_filename)
                        os.rename(original_file_path, new_file_path)
                        logging.debug(f"Renamed {filename} to {new_filename}")


    @staticmethod
    def read_config_file(project_name):
        current_dir = os.getcwd()
        file_name = project_name + '.json'
        full_config_file_path = os.path.join(current_dir, project_name, "config", file_name)
        try:
                with open(full_config_file_path, "r") as f:
                    configurations = json.loads(f.read())

                return configurations, full_config_file_path
        except Exception as e:
            raise Exception( "Exception occurred while reading Config File: %s, Error:%s " % (full_config_file_path, str(e)))
    @staticmethod
    def write_to_config_file(configs, full_config_file_path):
        try:
            with open(full_config_file_path, "w") as f:
                configs_json = json.dumps(configs, indent=2)
                f.write(configs_json)
                logging.debug(f"Writing updates to config file completed.")
        except Exception as e:
                raise Exception( "Exception occurred while updating Config File: %s, Error:%s " % (full_config_file_path, str(e)))

    @staticmethod
    def update_template_by_project_name(configs, full_config_file_path, project_name):
        aiflow_dag_details = configs["aiflow-dag-details"]
        aiflow_dag_details["dag_id"] = project_name.replace('-', '_')

        airflow_task_details = configs.get("airflow-task-details", {})
        if airflow_task_details is not None:
            project_name_job = project_name.replace('_', '-')
            airflow_task_details[project_name_job] = airflow_task_details["pyspark-template"]
            
            pyspark_job_main_file_s3_path = airflow_task_details[project_name_job]["spark_details"]["spark_kubernetes_args"]["pyspark_job_main_file_s3_path"]
            update_pyspark_job_main_file_s3_path = pyspark_job_main_file_s3_path.replace(Constants.DEAULT_TEMPLATE_DIR_NAME, project_name)
            airflow_task_details[project_name_job]["spark_details"]["spark_kubernetes_args"]["pyspark_job_main_file_s3_path"] = update_pyspark_job_main_file_s3_path
            #Delete keys except the project_name_job
            keys_to_remove = [key for key in airflow_task_details.keys() if key != project_name_job]
            for key in keys_to_remove:
                del airflow_task_details[key]
            # update schema dir path
            old_s3_schema_file_path =  airflow_task_details[project_name_job]["spark_details"]["spark_job_args"]["s3_schema_file_path"]
            new_s3_schema_file_path = old_s3_schema_file_path.replace(Constants.DEAULT_TEMPLATE_DIR_NAME, project_name)
            # update file name
            new_s3_schema_file_path = new_s3_schema_file_path.replace((Constants.DEAULT_TEMPLATE_DATA_SCHEMA_FILE_NAME + ".json"), (project_name.replace('-', '_') + "_schema.json"))
            airflow_task_details[project_name_job]["spark_details"]["spark_job_args"]["s3_schema_file_path"] = new_s3_schema_file_path
            # add project_dir_name, taks_name, schema_file_object_key
            airflow_task_details[project_name_job]["spark_details"]["spark_job_args"]["project_dir_name"] = project_name
            airflow_task_details[project_name_job]["spark_details"]["spark_job_args"]["task_name"] = project_name
            # airflow_task_details[project_name_job]["spark_details"]["spark_job_args"]["schema_file_object_key"] = project_name

             
            configs["airflow-task-details"] = airflow_task_details
            configs["aiflow-dag-details"] = aiflow_dag_details
            
        return configs
     

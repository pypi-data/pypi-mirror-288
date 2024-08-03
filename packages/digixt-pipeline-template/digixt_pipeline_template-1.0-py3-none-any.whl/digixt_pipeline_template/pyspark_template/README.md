**Author** - Hemanth Bommireddy
**Modified**

Common DAG Module:
-----------------
**aiflow-task-dependencies-details**

1. By default, if we don't provide , it will keep al the tasks run in Parallel.
2. Airflow task Dependencies, Provide as parent-child relationship for every node.
             "aiflow-task-dependencies-details": {
                                  "parent-child-relation":{
                                       "cargo_tracking_latest": ["start", "end"],
                                      "floating_storage_vessels_latest": ["start", "end"]
                              } }

3. Airflow task dependencies - Provide Task dependencies to run keep it as sequential.  
                     "aiflow-task-dependencies-details": {
                                 "task-auto-dependencies":{"trigger_order": "sequential"}
                              } }
4. Airflow task dependencies - Provide Task dependencies to run keep it as Parallel with config as number per each group.  
   a. trigger_rule is "all_done" means id all predecessors is just completed , then successor will trigger irrespective of success or failure.
                        "aiflow-task-dependencies-details": {
                                    "task-auto-dependencies":{"trigger_order": "parallel", "max_tasks_per_group": 3, "trigger_rule":  "all_done"}
                                 }
                              }


Spark Jobs:
-----------
1. "spark_kubernetes_args"  - Config values to submit spark jobs in Kubernetes. If we dont' provide , it will take default values.
 
   * Default values for spark drive and executor resources.
   * Default values for Kubernetes scheduler options.
   * Default Spark job main script.
   
2. "spark_job_args" - Spark job arguments.
   * "python_dependencies_base_paths" - Default python utils path will provide to spark job as dependency if we don't provide.
   * "project_dir_name" - The must be the project directory name. This is mandatory to package the project and add to spark PyFile so that it will ship the entire project to every 
   executor.
   
  *    
    
Usage of the Airflow Pipelines:
-------------------------------

1.  Config Json file (Directory: <project_name>\config\)
  a. Currently, pipelines are executing all sql files through Trino and Using "python details". 
  b. Provide airflow task name and target_table name for python operator. It will find the transform.sql path based on directory structure.
  c. Provide "aiflow-task-dependencies-details" accordingly. if not provided, it will keep all tasks as default configured.

2. Dag file/ flows file (Directory: <project_name>\flows\)
   a. create a new dag file , make sure config file name and dag file name should be same except extension.
            
           config file: aspect_pipeline.json
           dag file   : aspect_pipeline.py
   b. Follow the existing directory structure for to keep <project_name>.sql files.
      
          <project_name>/scripts/sql/<project_name>.sql
          <project_name>/scripts/sql/<project_name>.sql


Aiflow task retries:
--------------------

1. Provide retries and retry_delay at dag level as below , retry_delay in seconds. Default from Airflow is 300 seconds.
        "pyspark_template": {
        "start_date": "2023-07-25 00:00:00", 
        "schedule_interval": "30 4 * * *", 
        "tags":["pyspark_template", "template"], 
        "retries": 2, 
        "retry_delay": 900 
    }
2. If we don't provide them at dag level as in above step-1, it will consider from "AIRFLOW_DAG_DEFAULT_ARGS"
       {
        "max_active_runs": 1,
         "retries": 1,
        }
3. If values are not available in above both steps, kept default values.
    "retries": 1
    "retry_delay": it takes airflow default value

4. If start_date is not provided in the dag level, it will take a default value 30 days back from the current time, when the job is runing.
   

Airflow Dataset Trigger 
-----------------------

1. Parent DAG - Add a flag in airflow variable (DAG level) to track dataset outlet.
      "parent-dag-name": {
           "start_date": "2023-07-01 00:00:00",
           "schedule_interval": "00 02 * * *",
           "dataset_outlet_flag": true,
           "tags": []
       }
      
2. Child DAG - Update DAG schedule from Schedule interval to Schedule_dataset.

    "child-dag-name": {
          "start_date": "2023-10-16 00:00:00",
          "schedule_dataset": ["parent-dag-name"],
          "tags": []
       }




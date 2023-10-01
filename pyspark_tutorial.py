import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator, DataprocClusterDeleteOperator, DataProcPySparkOperator
from airflow.operators.python_operator import PythonOperator
from pyspark.sql import SparkSession


# Define default_args
default_args = {
    'owner': 'nurulfitrif',
    'depends_on_past': False,
    'start_date': yesterday,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Initialize a DAG
dag = DAG(
    'pyspark_wordcount',
    default_args=default_args,
    description='PySpark Word Count DAG',
    schedule_interval=timedelta(days=1),  # Run daily
)

# Create a Dataproc cluster creation task
create_dataproc_cluster = DataprocClusterCreateOperator(
    task_id='create_dataproc_cluster',
    cluster_name='pyspark-wordcount-cluster',
    num_workers=2,
    region='us-east1',
    zone=models.Variable.get('gce_zone'),
    image_version='2.0',
    master_machine_type='e2-standard-2',
    worker_machine_type='e2-standard-2',
    storage_bucket='qwiklabs-gcp-03-cf5f6485140a',
    dag=dag,
)

# Create a PySpark task 
run_pyspark_task = DataProcPySparkOperator(
    task_id='run_pyspark_job',
    main="gs://qwiklabs-gcp-03-cf5f6485140a/pyspark/pyspark_tutorial.py", 
    cluster_name='pyspark-wordcount-cluster',
    dataproc_pyspark_jars="gs://spark-lib/bigquery/spark-bigquery-latest.jar",
    region='us-east1', 
    dag=dag,
)

# Create a Dataproc cluster deletion task
delete_dataproc_cluster = DataprocClusterDeleteOperator(
    task_id='delete_dataproc_cluster',
    cluster_name='pyspark-wordcount-cluster',
    region='us-east1',
    trigger_rule='all_done',
)

# Define the task execution sequence
create_dataproc_cluster >> run_pyspark_task >> delete_dataproc_cluster

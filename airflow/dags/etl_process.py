import datetime
import json

from airflow import DAG
from airflow.operators.bash import BashOperator
# from airflow.hooks.base_hook import BaseHook

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    # 'on_failure_callback': task_fail_slack_alert,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=1),
    "email": ["andrea.guzzo92@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
}

# DAG configuration
dag = DAG(
    dag_id="etl_dag_rapids",
    default_args=default_args,
    # start_date=days_ago(1),
    start_date=datetime.datetime(2021, 7, 30, hour=12, minute=30, second=0),
    schedule_interval="@once",
    tags=["import_pipeline"],
)

# Operators configuration
extract_blob = BashOperator(
    task_id="extract_blob",
    bash_command="python /opt/airflow/dags/jobs/extract_blob.py",
    dag=dag,
)

extract_db = BashOperator(
    task_id="extract_db",
    bash_command="python /opt/airflow/dags/jobs/extract_db.py",
    dag=dag,
)

process_data = BashOperator(
    task_id="process_data",
    bash_command="python /opt/airflow/dags/jobs/process_data.py",
    dag=dag,
)

import_db = BashOperator(
    task_id="import_db",
    bash_command="python /opt/airflow/dags/jobs/import_db.py",
    dag=dag,
)

# graph configuration
[extract_blob, extract_db] >> process_data >> import_db

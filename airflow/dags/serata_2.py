from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSensorTimeout
from airflow.operators.dummy import DummyOperator
from airflow.contrib.sensors.file_sensor import FileSensor

from airflow.dags.jobs.extract_blob import launch_blob
from airflow.dags.jobs.check_stuff import check_variables
from airflow.dags.jobs.import_db import insert_db
from airflow.dags.jobs.extract_db import extract_db

FILE_PATH = "/opt/airflow/data"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime.now(),
    "email": ["pythonbiellagroup@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=2),
}


# Operators configuration
def _failure_callback(context):
    if isinstance(context["exception"], AirflowSensorTimeout):
        print(context)
    print("Sensor timed out")


dag = DAG(
    "pipeline_lombardia",
    start_date=datetime.now(),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
)

run_variables_check = PythonOperator(
    task_id="variable_check",
    python_callable=check_variables,
    dag=dag,
    op_kwargs={"state": "state_test"},
)

run_ospedali_extractor = BashOperator(
    task_id="ospedali_extractor",
    bash_command="python /opt/airflow/dags/jobs/extract_csv.py launch_ospedali",
    dag=dag,
)

run_popolazione_extractor = PythonOperator(
    task_id="popolazione_extractor", python_callable=launch_blob, dag=dag
)

run_performance_extractor = PythonOperator(
    task_id="performance_extractor", python_callable=extract_db, dag=dag
)


save_result_db = PythonOperator(
    task_id="save_result_db", python_callable=insert_db, dag=dag
)

## REMEMBER TO CREATE A file_check (fs) connection on admin > connections
sensor_extract_ospedali = FileSensor(
    task_id="sensor_extract_ospedali",
    mode="reschedule",
    on_failure_callback=_failure_callback,
    filepath="/opt/airflow/data/ospedali_result.csv",
    poke_interval=15,
    timeout=15 * 60,
    fs_conn_id="file_check",
)
sensor_extract_popolazione = FileSensor(
    task_id="sensor_extract_popolazione",
    mode="reschedule",
    on_failure_callback=_failure_callback,
    filepath="/opt/airflow/data/popolazione.csv",
    poke_interval=15,
    timeout=15 * 60,
    fs_conn_id="file_check",
)

sensor_extract_performance = FileSensor(
    task_id="sensor_extract_performance",
    mode="reschedule",
    on_failure_callback=_failure_callback,
    filepath="/opt/airflow/data/performance_dataset.csv",
    poke_interval=15,
    timeout=15 * 60,
    fs_conn_id="file_check",
)

start_op = DummyOperator(task_id="start_task", dag=dag)
mid_op = DummyOperator(task_id="mid_task", dag=dag)
last_op = DummyOperator(task_id="last_task", dag=dag)


(
    start_op
    >> run_variables_check
    >> run_ospedali_extractor
    >> sensor_extract_ospedali
    >> mid_op
    >> save_result_db
    >> last_op
)

(
    start_op
    >> run_variables_check
    >> run_popolazione_extractor
    >> sensor_extract_popolazione
    >> mid_op
    >> save_result_db
    >> last_op
)

(
    start_op
    >> run_variables_check
    >> run_performance_extractor
    >> sensor_extract_performance
    >> mid_op
    >> save_result_db
    >> last_op
)

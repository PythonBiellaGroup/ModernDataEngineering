from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSensorTimeout
from airflow.operators.dummy import DummyOperator
from airflow.contrib.sensors.file_sensor import FileSensor

from airflow.dags.jobs.extract_blob import launch_blob
from airflow.dags.jobs.check_stuff import check_variables

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
    task_id="variable_check", python_callable=check_variables, dag=dag
)

run_csv_extractor = BashOperator(
    task_id="bash_extractor",
    bash_command="python /opt/airflow/dags/jobs/extract_csv.py launch_ospedali",
    dag=dag,
)

run_blob_extractor = PythonOperator(
    task_id="python_extractor", python_callable=launch_blob, dag=dag
)

## REMEMBER TO CREATE A file_check (fs) connection on admin > connections
sensor_extract_csv = FileSensor(
    task_id="sensor_extract_ospedali",
    mode="reschedule",
    on_failure_callback=_failure_callback,
    filepath="/opt/airflow/data/ospedali.csv",
    poke_interval=15,
    timeout=15 * 60,
    fs_conn_id="file_check",
)
sensor_extract_blob = FileSensor(
    task_id="sensor_extract_popolazione",
    mode="reschedule",
    on_failure_callback=_failure_callback,
    filepath="/opt/airflow/data/popolazione_lombardia.csv",
    poke_interval=15,
    timeout=15 * 60,
    fs_conn_id="file_check",
)

start_op = DummyOperator(task_id="start_task", dag=dag)
mid_op = DummyOperator(task_id="mid_task", dag=dag)
last_op = DummyOperator(task_id="last_task", dag=dag)

# run_this_task_too = PythonOperator(
#     task_id="run_this_last", python_callable=run_also_this_func
# )

run_variables_check
start_op >> run_csv_extractor >> sensor_extract_csv >> mid_op
start_op >> run_variables_check >> run_blob_extractor >> sensor_extract_blob >> mid_op

import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": dt.datetime.now(),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    # "retry_delay": dt.timedelta(minutes=5),
}

dag = DAG(
    "simple_example",
    # schedule_interval="0 0 * * *",
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
)

launch_command = "printenv"

t1 = BashOperator(
    task_id="first_task", bash_command=launch_command, queue="new_queue", dag=dag
)


[t1]

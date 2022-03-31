import datetime
from datetime import timedelta
from airflow.models import DAG

# from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

args = {
    "owner": "airflow",
    "start_date": datetime.datetime.now(),
    "depends_on_past": False,
    "retry_delay": timedelta(minutes=1),
    "retries": 1,
}

dag = DAG(
    dag_id="python_sample_dag",
    start_date=datetime.datetime.now(),
    default_args=args,
    schedule_interval=None,
)


def run_this_func():
    print("I am coming first")


def run_also_this_func():
    print("Ciao Python Biella Group")
    print("I am coming last")


def hello_PBG():
    print("Ciao Python Biella Group")


with dag:
    run_this_task = PythonOperator(
        task_id="run_this_first", python_callable=run_this_func
    )
    run_this_task_too = PythonOperator(
        task_id="run_this_last", python_callable=run_also_this_func
    )
    run_PBG = PythonOperator(task_id="run_PBG", python_callable=run_also_this_func)

run_this_task >> run_this_task_too >> run_PBG

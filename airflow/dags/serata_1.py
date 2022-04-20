import os
import pandas as pd
import json
from datetime import datetime, timedelta

from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSensorTimeout
from airflow.operators.dummy import DummyOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.models.connection import Connection

c = Connection(
    conn_id="some_conn",
    conn_type="fs",
    description="FileSensor file system connection",
    host="myhost.com",
    login="admin",
    password="admin",
    extra=json.dumps(dict(this_param="some val", that_param="other val*")),
)
print(f"AIRFLOW_CONN_{c.conn_id.upper()}='{c.get_uri()}'")


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


def save_data(df: pd.DataFrame, filename: str = "data.csv", data_path: str = FILE_PATH):
    data_path = data_path
    data_file = filename
    file_path = os.path.join(data_path, data_file)
    df.to_csv(file_path, index=False)
    return df


def extract_data(filename: str = "extracted.csv"):
    df = pd.read_excel(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx",
        nrows=1000,
    )
    df = save_data(df, filename=filename)
    return df


def transform_data(df: pd.DataFrame, filename: str = "transformed.csv"):
    file_name = os.path.join(FILE_PATH, filename)
    df = pd.read_csv(file_name)
    df["TotalAmount"] = df["UnitPrice"] * df["Quantity"]
    df.drop(
        columns=["StockCode", "Description", "Country", "UnitPrice", "Quantity"],
        inplace=True,
    )
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"]).dt.date
    df["CustomerID"] = df["CustomerID"].astype("Int64")
    df = save_data(df, filename=filename)
    return df


def group_data(df: pd.DataFrame, filename: str = "aggregated.csv"):
    file_name = os.path.join(FILE_PATH, filename)
    df = pd.read_csv(file_name)
    df_aggr = df.groupby(["InvoiceNo", "InvoiceDate", "CustomerID"])[
        "TotalAmount"
    ].sum()
    save_data(df_aggr, filename=filename)
    return df


dag = DAG(
    "pipeline_serata",
    start_date=datetime.now(),
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args,
)

run_bash_extractor = BashOperator(
    task_id="bash_extractor",
    bash_command="python /opt/airflow/dags/jobs/process_data.py extract_data",
    dag=dag,
)

run_python_extractor = PythonOperator(
    task_id="python_extractor", python_callable=extract_data, dag=dag
)

run_python_transform = PythonOperator(
    task_id="python_transform", python_callable=transform_data, dag=dag
)

run_python_group = PythonOperator(
    task_id="python_group", python_callable=group_data, dag=dag
)

sensor_extract = FileSensor(
    task_id="sensor_extract",
    mode="reschedule",
    on_failure_callback=_failure_callback,
    filepath="/opt/airflow/data/extracted.csv",
    poke_interval=15,
    timeout=15 * 60,
    fs_conn_id="some_conn",
)

start_op = DummyOperator(task_id="start_task", dag=dag)
mid_op = DummyOperator(task_id="mid_task", dag=dag)
last_op = DummyOperator(task_id="last_task", dag=dag)

# run_this_task_too = PythonOperator(
#     task_id="run_this_last", python_callable=run_also_this_func
# )

(
    start_op
    >> run_python_extractor
    >> sensor_extract
    >> [run_python_transform, run_python_group]
    >> last_op
)

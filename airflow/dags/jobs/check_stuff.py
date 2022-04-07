from airflow.dags.common import config
from airflow.models import Variable


def check_variables():
    print(f"Airflow folder: {config.AIRFLOW_FOLDER}")
    print(f"Dag folder: {config.DAGS_FOLDER}")
    print(f"Data folder: {config.DATA_FOLDER}")
    
    TESTONE = Variable.get("TESTONE")
    TESTONE_NEW = Variable.set("TESTONE_NEW", "nuovo testone")
    print(f"TESTONE: {TESTONE}")
    print(f"TESTONE: {TESTONE_NEW}")
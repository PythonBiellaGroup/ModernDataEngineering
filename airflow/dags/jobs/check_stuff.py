from airflow.dags.common import config
from airflow.models import Variable


# Test variables, state and xcom passing values
def check_variables(state, ti):
    print(f"Airflow folder: {config.AIRFLOW_FOLDER}")
    print(f"Dag folder: {config.DAGS_FOLDER}")
    print(f"Data folder: {config.DATA_FOLDER}")

    TESTONE = Variable.get("TESTONE")
    # TESTONE_NEW = Variable.set("TESTONE_NEW", state)
    print(f"TESTONE: {TESTONE}")
    # print(f"TESTONE: {TESTONE_NEW}")

    ti.xcom_push(key="TESTONE", value=TESTONE)

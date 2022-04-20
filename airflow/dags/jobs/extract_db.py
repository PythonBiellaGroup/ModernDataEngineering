import pandas as pd
from airflow.dags.common import db, utils


def rename_columns(df):
    df.rename(
        columns={"PERIODO": "ANNO", "CODICE_STRUTTURA": "COD_STRUTTURA"}, inplace=True
    )
    return df


def drop_columns(df):
    df.drop(columns=["DENOMINAZIONE_STRUTTURA"], inplace=True)
    return df


def extract_db(ti):

    cxn = db.establish_external_db_connection()

    df = pd.read_sql_query("SELECT * FROM dbo.EXT_PERFORMANCE_HOSPITAL", con=cxn)
    cxn.dispose()

    df = rename_columns(df)
    df = drop_columns(df)

    # save to disk
    utils.save_result(df, "ospedali_result.csv")
    ti.xcom_push(key="performance_dataset", value="performance_dataset.csv")

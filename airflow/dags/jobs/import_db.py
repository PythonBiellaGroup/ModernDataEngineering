import os
import pandas as pd
import sqlalchemy
from airflow.dags.common import db
from airflow.dags.common import config


def insert_db(ti):

    try:
        cxn = db.establish_db_connection()

        ospedali_dataset = ti.xcom_pull(key="ospedali_dataset")
        popolazione_dataset = ti.xcom_pull(
            key="popolazione_dataset", task_ids="popolazione_extractor"
        )
        performance_dataset = ti.xcom_pull(key="performance_dataset")

        datasets = [ospedali_dataset, popolazione_dataset, performance_dataset]

        for dataset in datasets:

            # read the dataset
            file_path = os.path.join(config.DATA_FOLDER, dataset)
            df = pd.read_csv(file_path)

            # truncate the table if exist (remove it)
            dataset_name = dataset.upper().strip().split(".")[0]
            truncate_query = sqlalchemy.text(f"TRUNCATE TABLE {dataset_name}")
            cxn.execution_options(autocommit=True).execute(truncate_query)

            # insert the dataset into the sql table
            df.to_sql(dataset_name, con=cxn, if_exists="append", index=False)

        cxn.dispose()

    except Exception as message:
        raise Exception(f"Impossible to insert into db: {message}")

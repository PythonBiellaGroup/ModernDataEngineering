import os
import pandas as pd
import sqlalchemy
from airflow.dags.common import db
from airflow.dags.common import config


def insert_db(ti):

    try:
        cxn = db.establish_db_connection()

        # ospedali_dataset = ti.xcom_pull(key="ospedali_dataset")
        popolazione_dataset = ti.xcom_pull(
            key="popolazione_dataset", task_ids="popolazione_extractor"
        )
        performance_dataset = ti.xcom_pull(key="performance_dataset")

        # ospedali_dataset
        datasets = [popolazione_dataset, performance_dataset]

        print(f"Dataset names: f{datasets}")

        for dataset in datasets:
            print(f"Inserting dataset: {dataset}")

            # read the dataset
            file_path = os.path.join(config.DATA_FOLDER, dataset)
            df = pd.read_csv(file_path)

            # truncate the table if exist (remove it)
            dataset_name = dataset.upper().strip().split(".")[0]
            truncate_query = sqlalchemy.text(f"TRUNCATE TABLE {dataset_name}")
            cxn.execution_options(autocommit=True).execute(truncate_query)

            # insert the dataset into the sql table
            df.to_sql(dataset_name, con=cxn, if_exists="append", index=False)

            print(f"Dataset: {dataset} inserted successfully")

        cxn.dispose()
        print("All dataset inserted")
    except Exception as message:
        raise Exception(f"ERROR: Impossible to insert into db: {message}")

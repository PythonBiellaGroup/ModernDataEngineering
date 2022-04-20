import os
import pandas as pd
from airflow.dags.common import config
from airflow.dags.common import utils
from azure.storage.blob import BlobServiceClient


def download_file_blob():
    connect_str = config.BLOB_CONN_STR
    local_folder = config.DATA_FOLDER
    blob_container = config.BLOB_CONTAINER
    blob_name = config.BLOB_NAME
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(
        container=blob_container, blob=blob_name
    )

    try:
        download_file_path = os.path.join(local_folder, "popolazione_lombardia.csv")

        print("file path", download_file_path)
        print("\nDownloading blob to \n\t" + download_file_path)

        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

    except Exception as e:
        print(f"Impossible to launch blob download: {e}")
        raise Exception(e)

    return True


def read_file_blob():
    local_folder = config.DATA_FOLDER
    # read the file
    df = pd.read_csv(os.path.join(local_folder, "popolazione_lombardia.csv"))
    # some preprocessing
    df.drop(columns=["COORDINATA X", "COORDINATA Y", "POSIZIONE"], inplace=True)
    df.rename(
        columns={"FASCIA D'ETA'": "FASCIA_ETA", "% POPOLAZIONE": "PERC_POPOLAZIONE"},
        inplace=True,
    )
    return df


def launch_blob(ti):
    download_file_blob()
    df = read_file_blob()
    filename = "popolazione.csv"
    utils.save_result(df, filename)

    ti.xcom_push(key="popolazione_dataset", value=filename)

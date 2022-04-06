import os


AIRFLOW_FOLDER: str = os.path.abspath("../..")
DAGS_FOLDER: str = os.path.join(AIRFLOW_FOLDER, "dags")
DATA_FOLDER: str = os.path.join(DAGS_FOLDER, "data")

DB_ADDRESS: str = os.getenv("DB_ADDRESS", "localhost")
DB_NAME: str = os.getenv("DB_NAME", "test")
DB_NAME_EXTERNAL: str = os.getenv("DB_NAME_EXTERNAL", "test")
DB_USER: str = os.getenv("DB_USER", "admin")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "admin")
DB_DRIVER: str = "{ODBC Driver 17 for SQL Server}"

BLOB_CONN_STR: str = os.getenv("BLOB_CONN_STR", "test")
BLOB_CONTAINER: str = os.getenv("BLOB_CONTAINER", "")
BLOB_NAME: str = os.getenv("BLOB_NAME", "")

API_URL: str = os.getenv(
    "API_URL", "https://www.dati.lombardia.it/resource/6n7g-5p5e.json"
)
LINK_WEB: str = os.getenv(
    "LINK_WEB",
    "https://www.dati.lombardia.it/Sanit-/Dataset-condizioni-di-salute-per-provincia-e-gener/92eu-vwkf",
)

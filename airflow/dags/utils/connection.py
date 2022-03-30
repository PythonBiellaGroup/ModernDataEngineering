import urllib
# import pyodbc
# import pandas as pd
from sqlalchemy import create_engine
from .config import settings


def establish_db_connection():
    server = "airadav-work.database.windows.net"
    database = "hospitalization-lombardy"
    username = "admindav"
    password = "Password01"

    driver = "{ODBC Driver 17 for SQL Server}"

    odbc_str = (
        "DRIVER="
        + driver
        + ";SERVER="
        + server
        + ";PORT=1433;UID="
        + username
        + ";DATABASE="
        + database
        + ";PWD="
        + password
    )
    connect_str = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote(odbc_str)
    engine = create_engine(connect_str, echo=True)
    return engine


def establish_external_db_connection(
    server: str = settings.DB_SERVER,
    database: str = settings.DB_NAME,
    username: str = settings.DB_USER,
    password: str = settings.DB_PASSWORD,
):

    driver = "{ODBC Driver 17 for SQL Server}"

    odbc_str = (
        "DRIVER="
        + driver
        + ";SERVER="
        + server
        + ";PORT=1433;UID="
        + username
        + ";DATABASE="
        + database
        + ";PWD="
        + password
    )
    connect_str = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote(odbc_str)
    engine = create_engine(connect_str, echo=True)
    return engine

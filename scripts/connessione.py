import sqlalchemy
from sqlalchemy import create_engine
import urllib
import urllib.parse
import pyodbc

def establish_db_connection():
  server = "airadav-work.database.windows.net"
  database = "hospitalization-lombardy"
  username = "admindav"
  password = "Password01"

  driver = '{ODBC Driver 17 for SQL Server}'

  odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
  connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote(odbc_str)
  engine = create_engine(connect_str,echo = True)
  return engine

cxn= establish_db_connection()
df_performance_hospital = pd.read_sql_query("SELECT * FROM dbo.EXT_PERFORMANCE_HOSPITAL",con=cxn)
cxn.dispose()
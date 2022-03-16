from sqlalchemy import create_engine
import pandas as pd

# Get data from external database
cxn= establish_external_db_connection()
df_performance_hospital = pd.read_sql_query("SELECT * FROM dbo.EXT_PERFORMANCE_HOSPITAL",con=cxn)
cxn.dispose()

# Apply trasformations

def rename_columns(df):
  df.rename(columns={'PERIODO': 'ANNO','CODICE_STRUTTURA':'COD_STRUTTURA'},inplace=True)
  return df
#------------------------------------------------------------------------------------------------------------------------------------------ 
def drop_columns(df):
  df.drop(columns = ['DENOMINAZIONE_STRUTTURA'],inplace=True)
  return df

rename_columns(df_performance_hospital)
drop_columns(df_performance_hospital)

# Load the data into the destination database

cxn= establish_db_connection()
truncate_query = sqlalchemy.text("TRUNCATE TABLE WRH_PERFORMANCE_HOSPITAL")
cxn.execution_options(autocommit=True).execute(truncate_query)
df_performance_hospital.to_sql('WRH_PERFORMANCE_HOSPITAL',con=cxn,if_exists = 'append',index=False)
cxn.dispose()
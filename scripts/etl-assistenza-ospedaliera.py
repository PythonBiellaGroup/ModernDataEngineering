import os
import pandas as pd
from sodapy import Socrata

data_url = 'dati.lombardia.it'                        # The Host Name for the API endpoint (the https:// part will be added automatically)
data_set = '3rtw-8p48'                                # The data set at the API endpoint
app_token =  os.getenv('qEei2HKE5SldzRBJyNJqp9Wjw')   # The app token
limit_rows = 100000

#Extract

client = Socrata(data_url,app_token)
# Set the timeout to 60 seconds    
client.timeout = 60
# The SoDaPy library converts this CSV object to a Python list of dictionaries
results = client.get(data_set,limit=limit_rows)
# Convert the list of dictionaries to a Pandas data frame
df_ats_assistance = pd.DataFrame.from_records(results)

#Transform data

def rename_columns(df):
  df.rename(columns={'anno':'ANNO',
                     'codice_ats_residenza': 'COD_ATS',
                     'codice_acc_di_diagnosi': 'COD_ACC_DIAGNOSI',
                     'tasso_ricoveri_stessa_ats': 'TASSO_RICOVERI_STESSA_ATS',
                     'descrizione_acc_di_diagnosi': 'DESCRIZIONE_ACC_DI_DIAGNOSI',
                     'tasso_ricoveri_altra_ats': 'TASSO_RICOVERI_ALTRA_ATS'},inplace=True)
  return df
#------------------------------------------------------------------------------------------------------------------------------------------ 
def drop_columns(df):
  df.drop(columns = ['descrizione_ats_residenza',
                     'posizione_ats',
                     'coordinata_geografica_x',
                     'coordinata_geografica_y',
                     ':@computed_region_ttgh_9sm5',
                     ':@computed_region_6hky_swhk',
                     ':@computed_region_af5v_nc64'
                     ],inplace=True)
  return df

rename_columns(df_ats_assistance)
drop_columns(df_ats_assistance)

# Load data
cxn= establish_db_connection()
truncate_query = sqlalchemy.text("TRUNCATE TABLE WRH_ATS_DIAGNOSES")
cxn.execution_options(autocommit=True).execute(truncate_query)
df_ats_assistance.to_sql('WRH_ATS_DIAGNOSES',con=cxn,if_exists = 'append',index=False)
cxn.dispose()
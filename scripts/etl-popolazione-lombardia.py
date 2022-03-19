import sqlalchemy
import os
import pandas as pd
from azure.storage.blob import BlobServiceClient

current_dir = os.getcwd()
dump_folder = os.path.join(current_dir, 'data')

connect_str = 'DefaultEndpointsProtocol=https;AccountName=storagesanita;AccountKey=OB039ClwPwmVRQGSuG8cAhYPTEc3KGaD30/fp1USpiXGySK1Hb/f+cjS/XyAmR9kdce1g0qPn1drV/vLKrbpng==;EndpointSuffix=core.windows.net'
#Extract the file

def download_file_from_Azure(local_path,conn_str):

  # Create the BlobServiceClient object which will be used to create a container client
  blob_service_client = BlobServiceClient.from_connection_string(connect_str)
  
  # Create a blob client using the local file name as the name for the blob
  blob_client = blob_service_client.get_blob_client(container='storage-lombardia',blob='popolazione_lombardia.csv')

  try:
      download_file_path = os.path.join(local_path,'popolazione_lombardia.csv')
      print('file path',download_file_path)
      print("\nDownloading blob to \n\t" + download_file_path)
      with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
  except Exception as e:
      print(e)

download_file_from_Azure(dump_folder,connect_str)

# Remove unuseful fields

df_demografia_popolazione = pd.read_csv(os.path.join(dump_folder,'popolazione_lombardia.csv'))
def drop_columns(df):
  df.drop(columns = ['COORDINATA X',
                     'COORDINATA Y',
                     'POSIZIONE'],inplace=True
          )
  return df
#------------------------------------------------------------------------------------------------------------------------------------------
def rename_columns(df):
  df.rename(columns={"FASCIA D'ETA'": 'FASCIA_ETA',
                     '% POPOLAZIONE': 'PERC_POPOLAZIONE'
                     },inplace=True)
  return df

rename_columns(df_demografia_popolazione)
drop_columns(df_demografia_popolazione)

#load the file to the Azure database

cxn= establish_db_connection()
truncate_query = sqlalchemy.text("TRUNCATE TABLE WRH_DEMO_LOMBARDIA")
cxn.execution_options(autocommit=True).execute(truncate_query)
df_demografia_popolazione.to_sql('WRH_DEMO_LOMBARDIA',con=cxn,if_exists = 'append',index=False)
cxn.dispose()
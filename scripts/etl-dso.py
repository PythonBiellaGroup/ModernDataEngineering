import sqlalchemy
import os
from azure.storage.blob import BlobServiceClient

current_dir = os.getcwd()
dump_folder = os.path.join(current_dir, 'data')

connect_str = 'DefaultEndpointsProtocol=https;AccountName=storagesanita;AccountKey=OB039ClwPwmVRQGSuG8cAhYPTEc3KGaD30/fp1USpiXGySK1Hb/f+cjS/XyAmR9kdce1g0qPn1drV/vLKrbpng==;EndpointSuffix=core.windows.net'

#Extract the file

def download_file_from_Azure(local_path,conn_str):

  # Create the BlobServiceClient object which will be used to create a container client
  blob_service_client = BlobServiceClient.from_connection_string(connect_str)
  
  # Create a blob client using the local file name as the name for the blob
  blob_client = blob_service_client.get_blob_client(container='storage-sanita-lombardia',blob='Dataset_SDO_Regione_Lombardia.csv')

  try:
      download_file_path = os.path.join(local_path,'Dataset_SDO_Regione_Lombardia.csv')
      print("\nDownloading blob to \n\t" + download_file_path)
      with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
  except Exception as e:
      print(e)

download_file_from_Azure(dump_folder,connect_str)

#load the file to the Azure database
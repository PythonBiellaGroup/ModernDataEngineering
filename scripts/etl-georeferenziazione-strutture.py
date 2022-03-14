import requests
import pandas as pd
import os
import json
import sqlalchemy
from sqlalchemy import create_engine
import urllib
import urllib.parse

current_dir = os.getcwd()
dump_folder = os.path.join(current_dir, 'data')

# Extract data

url = 'https://www.dati.lombardia.it/resource/6n7g-5p5e.json'
response = requests.get(url)

print('Status code: ' , response.status_code)

df_georef_strutture = pd.DataFrame(json.loads(response.content))
df_georef_strutture.to_csv(dump_folder + '/georeferenziazione_strutture.csv')

#Transform data
def drop_columns(df):
  df.drop(columns = ['geocoded_column',
                     ':@computed_region_ttgh_9sm5',
                     ':@computed_region_6hky_swhk',
                     ':@computed_region_uypf_y6ry',
                     'localita',
                     'cap',
                     'ats_struttura',
                     'descrizione_struttura_di',
                     'indirizzo'],inplace=True
          )
  return df
#------------------------------------------------------------------------------------------------------------------------------------------
def rename_columns(df):
  df.rename(columns={'codice_struttura_di_ricovero': 'COD_STRUTTURA',
                     'coordinata_geografica_x': 'COORDINATA_X',
                     'coordinata_geografica_y' : 'COORDINATA_Y'
                     },inplace=True)
  return df

rename_columns(df_georef_strutture)
drop_columns(df_georef_strutture)


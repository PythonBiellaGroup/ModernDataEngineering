import pandas as pd
import os
import numpy as np
from sqlalchemy import create_engine

current_dir = os.getcwd()
extract_folder = os.path.join(current_dir, 'data/ospedali.csv')

#Extract data
df_ospedali = pd.read_csv(extract_folder)

#Transform data

#------------------------------------------------------------------------------------------------------------------------------------------
def drop_columns(df):
  df.drop(columns = ['COD_SUB'],inplace=True)
  return df
#------------------------------------------------------------------------------------------------------------------------------------------
def transf_cod_struttura(df):
  df['COD_SUB'] = df['COD_SUB'].astype(str)
  df['COD_SUB'] = df['COD_SUB'].apply(lambda x: x.zfill(2))
  df['COD_STRUTTURA'] = df['COD_STRUTTURA'].astype(str)
  df['COD_STRUTTURA'] = df['COD_STRUTTURA'].apply(lambda x: x.zfill(6))
  df['COD_STRUTTURA'] = df['COD_STRUTTURA'] + '-' + df['COD_SUB']
  return df
#------------------------------------------------------------------------------------------------------------------------------------------
def transf_ps_pediatrico(df):
  conditions = [
                (df['PS_PEDIATRICO'] == 'X'),
                (df['PS_PEDIATRICO'] == 'Nan')
                ]
  values = [1,0]
  df['PS_PEDIATRICO'] = np.select(conditions, values)
  return df
#------------------------------------------------------------------------------------------------------------------------------------------
def transf_data_apertura_chiusura(df):
  df['DATA_APERTURA'] = pd.to_datetime(df['DATA_APERTURA']).dt.date
  df['DATA_CHIUSURA'] = pd.to_datetime(df['DATA_CHIUSURA']).dt.date
  df.fillna({'DATA_CHIUSURA':'2999-12-31'}, inplace=True)
  return df
#------------------------------------------------------------------------------------------------------------------------------------------
def add_descr_liv_emergenza(df):
   df['LIV_EMERG'].replace('Senza livello emergenza','SLE',inplace = True)
   df['DESCR_LIV_EMERG'] = df['LIV_EMERG']
   df['DESCR_LIV_EMERG'].replace({'DEA-PS': 'Dipartimento Emergenza Accettazione-Pronto Soccorso',
                                  'DEA-PS-PPI': 'Dipartimento Emergenza Accettazione-Pronto Soccorso-Punto di Primo Intervento',
                                  'EAS-PS': 'Emergenza Alta Specialità-Pronto Soccorso',
                                  'EAS-PS-PPI': 'Emergenza Alta Specialità-Pronto Soccorso-Punto di Primo Intervento',
                                  'PS-PPI': 'Pronto Soccorso-Punto di Primo Intervento',
                                  'PS': 'Pronto Soccorso',
                                  'PPI': 'Punto di Primo Intervento',
                                  'EAS': 'Emergenza Alta Specialità',
                                  'SLE': 'Senza Livello Emergenza'}, inplace=True)
   return df
#------------------------------------------------------------------------------------------------------------------------------------------
def rename_columns(df):
  df.rename(columns={'ATS': 'COD_ATS',
                     },inplace=True)
  return df

transf_cod_struttura(df_ospedali)
transf_ps_pediatrico(df_ospedali)
transf_data_apertura_chiusura(df_ospedali)
add_descr_liv_emergenza(df_ospedali)
drop_columns(df_ospedali)
rename_columns(df_ospedali)

#reorganize columns orders
df_ospedali = df_ospedali[['COD_STRUTTURA',
'DENOM_STRUTTURA',
'COD_ATS',
'COD_ENTE',
'DENOM_ENTE',
'COD_TIPO_STR',
'DESCR_TIPO_STR',
'DATA_APERTURA',
'DATA_CHIUSURA',
'INDIRIZZO',
'CAP',
'LOCALITA',
'FAX',
'LIV_EMERG',
'DESCR_LIV_EMERG',
'PS_PEDIATRICO'
]]

# Load data
#Write data into the table in AZURE SQL Server database
cxn= establish_db_connection()
truncate_query = sqlalchemy.text("TRUNCATE TABLE STG_ANG_HOSPITAL")
cxn.execution_options(autocommit=True).execute(truncate_query)
df_ospedali.to_sql('STG_ANG_HOSPITAL',con=cxn,if_exists = 'append',index=False)
cxn.dispose()
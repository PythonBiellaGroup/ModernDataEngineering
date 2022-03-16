import pandas as pd
import time
import datetime as dt
import math
import os
import warnings
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
warnings.filterwarnings("ignore")

current_dir = os.getcwd()
chromedriver_folder = os.path.join(current_dir, 'webdriver')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


linkweb = 'https://www.dati.lombardia.it/Sanit-/Dataset-condizioni-di-salute-per-provincia-e-gener/92eu-vwkf'
scrWidth = 1920
scrHeight = 1080
delay = 10

current_dir = os.getcwd()
dump_folder = os.path.join(current_dir, 'data/condizioni_provincie.csv')

# Extract data using scraping and Selenium

wd = webdriver.Chrome('/Users/davideairaghi/Documents/GitHub/ModernDataEngineering/webdriver/chromedriver',chrome_options=chrome_options)
wd.set_window_size(scrWidth, scrHeight)
wd.get(linkweb)

def extract_table_values(row):
  anno = ""
  provincia = ""
  genere = ""
  coordinata_x = ""
  coordinata_y = ""
  speranza_vita_nascita = ""
  tasso_mortalita = ""
  tasso_mortalita_infantile = ""
  posizione = ""
  date_loading = dt.date.today()
  
  try:
    anno = row.find_element_by_css_selector('td:nth-child(1)').text
    provincia = row.find_element_by_css_selector('td:nth-child(2)').text
    genere = row.find_element_by_css_selector('td:nth-child(3)').text
    coordinata_x = row.find_element_by_css_selector('td:nth-child(4)').text
    coordinata_y = row.find_element_by_css_selector('td:nth-child(5)').text
    speranza_vita_nascita = row.find_element_by_css_selector('td:nth-child(6)').text
    tasso_mortalita = row.find_element_by_css_selector('td:nth-child(7)').text
    tasso_mortalita_infantile = row.find_element_by_css_selector('td:nth-child(8)').text
    posizione = row.find_element_by_css_selector('td:nth-child(9)').text
  except:
    pass
  return {
          'date_loading': date_loading,
          'anno': anno,
          'provincia': provincia,
          'genere': genere,
          'coordinata_x': coordinata_x,
          'coordinata_y': coordinata_y,
          'speranza_vita_nascita': speranza_vita_nascita,
          'tasso_mortalita': tasso_mortalita,
          'tasso_mortalita_infantile': tasso_mortalita_infantile,
          'posizione':posizione
          }

rows_to_scrape = wd.find_element_by_css_selector('div > div > dl > div:nth-child(1) > dd')
num_rows = int(rows_to_scrape.text)
print('Total rows to scrape: ' + str(num_rows))

dataset_condizioni_salute_prov = []
num_pages = math.ceil(num_rows/13)
print('Number of pages: ',num_pages)
cnt = 0

for num in range(1,num_pages+1):
  table_socr = wd.find_element_by_css_selector("div.socrata-visualization-chart-container > div > table > tbody")
  t_cond_salute = table_socr.find_elements_by_tag_name("tr")
  for s in t_cond_salute:
    if cnt < num_rows:
      dataset_condizioni_salute_prov.append(extract_table_values(s))
      cnt = cnt +1
  next_button = wd.find_element_by_class_name('pager-button-next')
  if next_button.is_enabled():
    WebDriverWait(wd, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, "pager-button-next")))
    next_button.click()
    time.sleep(delay)

print('Total rows scraped: '+ str(cnt) + ' on total rows expected: ' + str(num_rows))

df_condizioni_salute_prov = pd.DataFrame(dataset_condizioni_salute_prov)
df_condizioni_salute_prov.to_csv(dump_folder)

wd.close()

# Transform data
def rename_columns(df):
  df.rename(columns={'date_loading':'DATE_LOADING',
                     'anno': 'ANNO',
                     'provincia':'PROVINCIA',
                     'genere':'GENERE',
                     'speranza_vita_nascita': 'SPERANZA_VITA_NASCITA',
                     'tasso_mortalita': 'TASSO_MORTALITA',
                     'tasso_mortalita_infantile': 'TASSO_MORTALITA_INFANTILE'},inplace=True)
  return df
#------------------------------------------------------------------------------------------------------------------------------------------ 
def drop_columns(df):
  df.drop(columns = ['coordinata_x',
                     'coordinata_y',
                     'posizione'
                     ],inplace=True)
  return df
#------------------------------------------------------------------------------------------------------------------------------------------ 
def convert_to_float(df):
    df['TASSO_MORTALITA'] = df['TASSO_MORTALITA'].apply(lambda x: x.replace(',','.'))
    df['TASSO_MORTALITA'] = df['TASSO_MORTALITA'].astype(float,errors='ignore')
    df['TASSO_MORTALITA_INFANTILE'] = df['TASSO_MORTALITA_INFANTILE'].apply(lambda x: x.replace(',','.'))
    df['TASSO_MORTALITA_INFANTILE'] = df['TASSO_MORTALITA_INFANTILE'].astype(float,errors='ignore')
    df['SPERANZA_VITA_NASCITA'] = df['SPERANZA_VITA_NASCITA'].apply(lambda x: x.replace(',','.'))
    df['SPERANZA_VITA_NASCITA'] = df['SPERANZA_VITA_NASCITA'].astype(float,errors='ignore')
    return df
#------------------------------------------------------------------------------------------------------------------------------------------ 
def round_tasso_mortalita(df):
  df['TASSO_MORTALITA'] = df['TASSO_MORTALITA'].apply(lambda x: np.round(x,decimals=2))
  return df


#Apply transformation

rename_columns(df_condizioni_salute_prov)
drop_columns(df_condizioni_salute_prov)
convert_to_float(df_condizioni_salute_prov)
round_tasso_mortalita(df_condizioni_salute_prov)


#Load data into

cxn= establish_db_connection()
truncate_query = sqlalchemy.text("TRUNCATE TABLE WRH_PROVINCE_HEALTH")
cxn.execution_options(autocommit=True).execute(truncate_query)
df_condizioni_salute_prov.to_sql('WRH_PROVINCE_HEALTH',con=cxn,if_exists = 'append',index=False)
cxn.dispose()
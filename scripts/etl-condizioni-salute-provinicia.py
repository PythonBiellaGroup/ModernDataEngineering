import pandas as pd
import time
import datetime as dt
import math
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

df_condizioni_salute_prov = pd.DataFrame(dataset_condizioni_salute_prov)
df_condizioni_salute_prov.head()

wd.close()
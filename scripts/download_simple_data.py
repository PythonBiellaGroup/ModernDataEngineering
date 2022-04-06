import pandas as pd
import datetime as dt


#load
df = pd.read_excel('https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx',nrows=1000)

#transformation
df['TotalAmount'] = df['UnitPrice']*df['Quantity']
df.drop(columns=['StockCode','Description','Country','UnitPrice','Quantity'],inplace=True)
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']).dt.date
df['CustomerID'] = df['CustomerID'].astype('Int64')

df_aggr = df.groupby(['InvoiceNo','InvoiceDate','CustomerID'])['TotalAmount'].sum()
df_aggr.head()
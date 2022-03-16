from sqlalchemy create_engine
from sqlalchemy import text

#Load the hospital domain table with the source available in staging area 

cxn= establish_db_connection()

sql = text('INSERT INTO dbo.ANG_HOSPITAL '
           'SELECT '
	         'ang.COD_STRUTTURA, '
	         'DENOM_STRUTTURA, '
	         'COD_ATS, '
	         'DESCR_ATS, '
	         'COD_ENTE, '
	         'DENOM_ENTE, '
	         'COD_TIPO_STR, '
	         'DESCR_TIPO_STR, '
	         'DATA_APERTURA, '
	         'DATA_CHIUSURA, '
	         'INDIRIZZO, '
	         'CAP, '
	         'LOCALITA, '
           'COORDINATA_X, '
           'COORDINATA_Y, '
	         'FAX, '
	         'LIV_EMERG, '
	         'DESCR_LIV_EMERG, '
	         'PS_PEDIATRICO '
          'FROM dbo.STG_ANG_HOSPITAL ang '
          'LEFT JOIN STG_GEOREF_STRUTTURE geo ' 
              'on geo.COD_STRUTTURA = ang.COD_STRUTTURA'
              )
cxn.execution_options(autocommit=True).execute(sql)

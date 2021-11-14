CREATE TABLE [dbo].[ANG_HOSPITAL]
(
	COD_STRUTTURA [char](9) not null PRIMARY KEY,
	DENOM_STRUTTURA [nvarchar](100),
	COD_ATS int,
	DESCR_ATS [nvarchar](100),
	COD_ENTE int,
	DENOM_ENTE [nvarchar](100),
    COD_TIPO_STR int,
	DESCR_TIPO_STR [nvarchar](100),
	DATA_APERTURA date,
	DATA_CHIUSURA date,
	INDIRIZZO [nvarchar](100),	
	CAP int,
	LOCALITA  [nvarchar](100),
	COORDINATA_X [nvarchar](100),
	COORDINATA_Y [nvarchar](100),
	FAX [nvarchar](50),
	LIV_EMERG [nvarchar](10),
	DESCR_LIV_EMERG [nvarchar](200),
	PS_PEDIATRICO char(1)
);
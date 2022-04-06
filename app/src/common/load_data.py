import pandas as pd


def load_demo_data(conn):
    df = pd.read_sql_query(
        "select ANNO,PROVINCIA,GENERE,FASCIA_ETA,POPOLAZIONE "
        "from [dbo].[WRH_DEMO_LOMBARDIA] "
        "where GENERE <> 'ALL' AND FASCIA_ETA <> 'ALL' "
        "order by FASCIA_ETA",
        con=conn,
    )
    return df


def load_livello_emergenza(conn):
    df = pd.read_sql_query(
        "select COUNT(1) as CONTEGGIO,DESCR_LIV_EMERG AS LIVELLO_EMERGENZA "
        "from [dbo].[ANG_HOSPITAL] "
        "GROUP BY DESCR_LIV_EMERG",
        con=conn,
    )
    return df


def load_provincie(conn):
    df = pd.read_sql_query(
        "select distinct PROVINCIA as PROVINCIA "
        "from [dbo].[WRH_PROVINCE_HEALTH] "
        "where PROVINCIA <> 'ITALIA' "
        "order by PROVINCIA",
        con=conn,
    )
    return df


def load_tipo_strutture(conn):
    df = pd.read_sql_query(
        "select COUNT(1) as CONTEGGIO,DESCR_TIPO_STR AS TIPO_STRUTTURA "
        "from [dbo].[ANG_HOSPITAL] "
        "GROUP BY DESCR_TIPO_STR",
        con=conn,
    )
    return df


def load_mortalita(conn):
    df = pd.read_sql_query(
        "select ANNO,PROVINCIA,GENERE,SPERANZA_VITA_NASCITA,TASSO_MORTALITA "
        "from [dbo].[WRH_PROVINCE_HEALTH] "
        "where GENERE = 'ALL'",
        con=conn,
    )
    return df


def load_strutture_geo(conn):
    df = pd.read_sql_query(
        "select * "
        "from [dbo].[ANG_HOSPITAL] "
        "where COORDINATA_X IS NOT NULL and COORDINATA_Y IS NOT NULL ",
        con=conn,
    )
    return df


def load_performance_ospedali(cod, conn):
    df = pd.read_sql_query(
        """select * 
            from [dbo].[VW_PERFORMANCE_OSPEDALI]
            where COD_STRUTTURA = ? """,
        con=conn,
        params=[cod],
    )
    return df


def load_ospedali(conn):
    df = pd.read_sql_query(
        "select cod_struttura,denom_struttura "
        "from ANG_HOSPITAL "
        "order by denom_struttura",
        con=conn,
    )
    return df


def load_gruppo_clinico(conn):
    df = pd.read_sql_query(
        "select CODICE_ACC_DI_DIAGNOSI,DESCRIZIONE_ACC_DI_DIAGNOSI "
        "from ANG_DIAGNOSI "
        "order by DESCRIZIONE_ACC_DI_DIAGNOSI",
        con=conn,
    )
    return df


def load_clinico(anno, cod, cod_acc_diagnosi, conn):
    df = pd.read_sql_query(
        """select
            codice_drg,
            descrizione_drg,
            codice_acc_di_diagnosi,
            descrizione_acc_di_diagnosi,
            sum(TOTALE_RICOVERI) as totale_ricoveri
        from WRH_SDO_HOSPITAL_LOMBARDY
        where anno = ? and CODICE_STRUTTURA_DI_RICOVERO = ? and codice_acc_di_diagnosi = ?
        group by
            codice_drg,
            descrizione_drg,
            codice_acc_di_diagnosi, 
            descrizione_acc_di_diagnosi """,
        con=conn,
        params=[anno, cod, cod_acc_diagnosi],
    )
    return df


def load_occupazione_repato_clinico(anno, cod, cod_diagnosi, conn):
    df = pd.read_sql_query(
        f"""select
            codice_disciplina,
            descrizione_disciplina,
            sum(totale_ricoveri) as totale_ricoveri
            from WRH_SDO_HOSPITAL_LOMBARDY
            where anno = ? and CODICE_STRUTTURA_DI_RICOVERO = ? and codice_acc_di_diagnosi = ?
                group by
                codice_disciplina, 
                descrizione_disciplina""",
        con=conn,
        params=[anno, cod, cod_diagnosi],
    )
    return df


def get_cod_ospedale(df, descr_struttura):
    cod_ospedale = df.loc[df["denom_struttura"] == descr_struttura][
        "cod_struttura"
    ].values[0]
    return cod_ospedale


def get_cod_gruppo_clinico(df, descr_clinico):
    cod_clinico = df.loc[df["DESCRIZIONE_ACC_DI_DIAGNOSI"] == descr_clinico][
        "CODICE_ACC_DI_DIAGNOSI"
    ].values[0]
    return cod_clinico

import os
import pandas as pd
import numpy as np
from airflow.dags.common import config
from airflow.dags.common import utils


def import_ospedali(file_path: str, file_name: str):
    file_path = os.path.join(file_path, file_name)
    df_ospedali = None
    if utils.check_if_file_exists(file_path):
        df_ospedali = pd.read_csv(file_path)
    else:
        raise Exception(f"import ospedali csv not found on: {file_path}")

    return df_ospedali


def drop_columns(df):
    df.drop(columns=["COD_SUB"], inplace=True)
    return df


def transf_cod_struttura(df):
    df["COD_SUB"] = df["COD_SUB"].astype(str)
    df["COD_SUB"] = df["COD_SUB"].apply(lambda x: x.zfill(2))
    df["COD_STRUTTURA"] = df["COD_STRUTTURA"].astype(str)
    df["COD_STRUTTURA"] = df["COD_STRUTTURA"].apply(lambda x: x.zfill(6))
    df["COD_STRUTTURA"] = df["COD_STRUTTURA"] + "-" + df["COD_SUB"]
    return df


def transf_ps_pediatrico(df):
    conditions = [(df["PS_PEDIATRICO"] == "X"), (df["PS_PEDIATRICO"] == "Nan")]
    values = [1, 0]
    df["PS_PEDIATRICO"] = np.select(conditions, values)
    return df


def transf_data_apertura_chiusura(df):
    df["DATA_APERTURA"] = pd.to_datetime(df["DATA_APERTURA"]).dt.date
    df["DATA_CHIUSURA"] = pd.to_datetime(df["DATA_CHIUSURA"]).dt.date
    df.fillna({"DATA_CHIUSURA": "2999-12-31"}, inplace=True)
    return df


def add_descr_liv_emergenza(df):
    df["LIV_EMERG"].replace("Senza livello emergenza", "SLE", inplace=True)
    df["DESCR_LIV_EMERG"] = df["LIV_EMERG"]
    df["DESCR_LIV_EMERG"].replace(
        {
            "DEA-PS": "Dipartimento Emergenza Accettazione-Pronto Soccorso",
            "DEA-PS-PPI": "Dipartimento Emergenza Accettazione-Pronto Soccorso-Punto di Primo Intervento",
            "EAS-PS": "Emergenza Alta Specialità-Pronto Soccorso",
            "EAS-PS-PPI": "Emergenza Alta Specialità-Pronto Soccorso-Punto di Primo Intervento",
            "PS-PPI": "Pronto Soccorso-Punto di Primo Intervento",
            "PS": "Pronto Soccorso",
            "PPI": "Punto di Primo Intervento",
            "EAS": "Emergenza Alta Specialità",
            "SLE": "Senza Livello Emergenza",
        },
        inplace=True,
    )
    return df


def rename_columns(df):
    df.rename(
        columns={
            "ATS": "COD_ATS",
        },
        inplace=True,
    )
    return df


def launch_ospedali(file_name: str, ti):
    if not file_name:
        file_name = "ospedali.csv"

    file_path = config.DATA_FOLDER

    # import the data
    df_ospedali = import_ospedali(file_path, file_name)

    # apply some transformations
    df_ospedali = transf_cod_struttura(df_ospedali)
    df_ospedali = transf_ps_pediatrico(df_ospedali)
    df_ospedali = transf_data_apertura_chiusura(df_ospedali)
    df_ospedali = add_descr_liv_emergenza(df_ospedali)
    df_ospedali = drop_columns(df_ospedali)
    df_ospedali = rename_columns(df_ospedali)

    # save the result
    result = utils.save_result(df_ospedali, "ospedali_result.csv")

    ti.xcom_push(key="ospedali_result", value="ospedali_result.csv")

    return result

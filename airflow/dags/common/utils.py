import os
import pandas as pd
from .config import DATA_FOLDER


def check_if_file_exists(file):
    if os.path.exists(file) and os.path.isfile(file):
        return True
    else:
        return False


def save_result(df: pd.DataFrame, filename: str):

    try:
        file_path = os.path.join(DATA_FOLDER, filename)
        df.to_csv(file_path, index=False)
        return True
    except Exception as message:
        raise Exception(f"Error while saving the result: {message}")
        return False

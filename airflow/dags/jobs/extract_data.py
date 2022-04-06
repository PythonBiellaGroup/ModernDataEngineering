import pandas as pd
import os


def extract_data():
    df = pd.read_excel(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx",
        nrows=1000,
    )
    data_path = "/opt/airflow/data"
    data_file = "extracted_data.csv"
    file_path = os.path.join(data_path, data_file)
    df.to_csv(file_path, index=False)
    return df


if __name__ == "__main__":
    extract_data()

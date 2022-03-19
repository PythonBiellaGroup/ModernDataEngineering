import os

import streamlit as st
import pandas as pd
from app.src.config import settings


@st.cache(persist=False, show_spinner=True)
def read_dataframe():

    data_path = os.path.join(settings.DATA_PATH, "tweet_cleaned.csv")
    df = pd.read_csv(data_path, sep="|")

    return df

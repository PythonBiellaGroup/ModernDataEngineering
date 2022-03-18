import streamlit as st
import pandas as pd
import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def vader_sentiment(
    sentence: list = ["Airtags are extremely useful and I love the design"],
):
    vd = SentimentIntensityAnalyzer()
    vader_result = vd.polarity_scores(sentence[0])
    print(
        "Overall scores: Compound={0:.2f}; Negative={1:.2f}; Neutral={2:.2f}; Positive={3:.2f} \n".format(
            vader_result["compound"],
            vader_result["neg"],
            vader_result["neu"],
            vader_result["pos"],
        )
    )

    return vader_result


def text_blob_sentiment(
    sentence: list = ["Airtags are extremely useful and I love the design"],
):
    score = TextBlob(sentence[0]).sentiment.polarity

    if score < 0:
        sentiment = "Negative"
    elif score == 0:
        sentiment = "Neutral"
    elif score > 0:
        sentiment = "Positive"

    print("Sentence Sentiment: {}".format(sentiment))
    print("Scores: {0:.2f}".format(score))

    return score, sentiment


def getSubjectivity(text: str):
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text: str):
    return TextBlob(text).sentiment.polarity


def getPolarityAnalysis(score: float):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    elif score > 0:
        return "Positive"


def getSubjectivityAnalysis(score: float):
    if score < 0.50:
        return "Objective"
    elif score == 0.50:
        return "Neutral"
    elif score > 0.50:
        return "Subjective"


def assignQuadrant(pol, subj):
    return pol + " and " + subj


@st.cache()
def text_blob_transformation(input_df: pd.DataFrame):
    df = input_df.copy()
    df.drop(["created_at", "tweet_preprocessed"], axis=1, inplace=True)
    df["subjectivity"] = df["tweet_cleaned"].apply(getSubjectivity)
    df["polarity"] = df["tweet_cleaned"].apply(getPolarity)
    df["polarity_analysis"] = df["polarity"].apply(getPolarityAnalysis)
    df["subjectivity_analysis"] = df["subjectivity"].apply(getSubjectivityAnalysis)
    df["type"] = np.vectorize(assignQuadrant)(
        df["polarity_analysis"], df["subjectivity_analysis"]
    )
    return df


def text_blob_count_results(df: pd.DataFrame):
    frequency_pol = df.groupby(["polarity_analysis"]).size().reset_index(name="cnt")
    frequency_sub = df.groupby(["subjectivity_analysis"]).size().reset_index(name="cnt")

    return frequency_pol, frequency_sub

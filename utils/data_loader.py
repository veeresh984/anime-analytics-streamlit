import pandas as pd
import streamlit as st

DATA_PATH = "data/anime_dataset.csv"

@st.cache_data
def load_data():
    """Load anime dataset with caching."""
    df = pd.read_csv(DATA_PATH)

    # Convert numeric columns
    numeric_cols = ["Score", "Members", "Popularity"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with missing titles
    df = df.dropna(subset=["Name"])

    return df

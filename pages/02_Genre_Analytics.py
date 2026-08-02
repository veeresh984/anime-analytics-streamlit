import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Genre Analytics", layout="wide")

df = load_data()

st.title("Genre Analytics")

genre_series = (
    df["Genres"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
)

genre_counts = genre_series.value_counts().reset_index()
genre_counts.columns = ["Genre", "Count"]

fig = px.bar(
    genre_counts.head(10),
    x="Genre",
    y="Count",
    title="Top Genres"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Anime by Genre")

selected_genre = st.selectbox(
    "Select Genre",
    sorted(genre_counts["Genre"].unique())
)

filtered = df[
    df["Genres"].str.contains(selected_genre, case=False, na=False)
]

st.dataframe(
    filtered[["Name", "Score", "Studios"]],
    use_container_width=True,
    hide_index=True
)

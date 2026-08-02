02_Genre_Analytics.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Genre Analytics", layout="wide")

df = load_data()

st.title("🎭 Genre Analytics")

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
    genre_counts.head(15),
    x="Genre",
    y="Count",
    title="Top 15 Genres",
    text="Count",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Average Score by Genre")

rows = []

for _, row in df.iterrows():
    if pd.notna(row["Genres"]):
        for g in str(row["Genres"]).split(","):
            rows.append([g.strip(), row["Score"]])

genre_score_df = pd.DataFrame(rows, columns=["Genre", "Score"])

avg_score = (
    genre_score_df.groupby("Genre")["Score"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig2 = px.bar(
    avg_score.head(15),
    x="Genre",
    y="Score",
    title="Highest Rated Genres",
    text_auto=".2f",
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

selected_genre = st.selectbox(
    "Select Genre",
    sorted(genre_counts["Genre"].unique()),
)

filtered = df[df["Genres"].str.contains(selected_genre, na=False)]

st.subheader(f"Anime in {selected_genre}")
st.dataframe(
    filtered[["Name", "Score", "Studios", "Members"]],
    use_container_width=True,
    hide_index=True,
)

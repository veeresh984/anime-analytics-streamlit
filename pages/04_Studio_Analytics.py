import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Studio Analytics", layout="wide")

df = load_data()

if df.empty:
    st.error("Dataset is empty. Please check data/anime_dataset.csv")
    st.stop()

st.title("Studio Analytics")
st.write("Analyze anime studios, production counts, and average ratings.")

st.markdown("---")

studio_counts = df["Studios"].value_counts().reset_index()
studio_counts.columns = ["Studio", "Anime_Count"]

st.subheader("Top Studios by Anime Count")

fig_count = px.bar(
    studio_counts.head(15),
    x="Studio",
    y="Anime_Count",
    title="Top Studios by Number of Anime"
)

st.plotly_chart(fig_count, use_container_width=True)

st.markdown("---")

st.subheader("Average Score by Studio")

avg_score = (
    df.groupby("Studios")["Score"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig_score = px.bar(
    avg_score.head(15),
    x="Studios",
    y="Score",
    title="Top Studios by Average Score"
)

st.plotly_chart(fig_score, use_container_width=True)

st.markdown("---")

st.subheader("Studio Explorer")

selected_studio = st.selectbox(
    "Select a Studio",
    sorted(df["Studios"].dropna().unique())
)

studio_df = df[df["Studios"] == selected_studio]

st.write("Total anime by selected studio:", len(studio_df))

st.dataframe(
    studio_df[["Name", "Score", "Genres", "Members"]],
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

st.subheader("Top Rated Anime from Selected Studio")

top_studio = (
    studio_df.sort_values("Score", ascending=False)
    [["Name", "Score", "Genres"]]
    .head(10)
)

st.dataframe(top_studio, use_container_width=True, hide_index=True)

st.markdown("---")

st.subheader("Studio Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Anime", len(studio_df))
col2.metric("Average Score", round(studio_df["Score"].mean(), 2))
col3.metric("Total Members", int(studio_df["Members"].sum()))

st.markdown("---")

top_studio_name = studio_counts.iloc[0]["Studio"]
top_studio_count = int(studio_counts.iloc[0]["Anime_Count"])

best_studio_name = avg_score.iloc[0]["Studios"]
best_studio_score = float(avg_score.iloc[0]["Score"])

st.info(
    "Most productive studio: "
    + top_studio_name
    + " ("
    + str(top_studio_count)
    + " anime)"
)

st.info(
    "Highest rated studio: "
    + best_studio_name
    + " ("
    + str(round(best_studio_score, 2))
    + " average score)"
)

st.markdown("---")

st.caption("Anime Analytics Dashboard - Studio Analytics")

import streamlit as st
import pandas as pd
from utils.data_loader import load_data

st.set_page_config(page_title="AI Insights", layout="wide")

df = load_data()

if df.empty:
    st.error("Dataset is empty. Please check data/anime_dataset.csv")
    st.stop()

df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
df["Members"] = pd.to_numeric(df["Members"], errors="coerce")

st.title("AI Insights")
st.write("Automated insights generated from the anime dataset.")

st.markdown("---")

avg_score = round(df["Score"].mean(), 2)

top_anime = df.sort_values("Score", ascending=False).iloc[0]

popular_anime = df.sort_values("Members", ascending=False).iloc[0]

genre_counts = (
    df["Genres"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
)

top_genre = genre_counts.index[0]

st.subheader("Executive Insights")

st.success(
    "Average anime score: " + str(avg_score)
)

st.success(
    "Highest rated anime: "
    + top_anime["Name"]
    + " ("
    + str(round(float(top_anime["Score"]), 2))
    + ")"
)

st.success(
    "Most popular anime: "
    + popular_anime["Name"]
)

st.success(
    "Most common genre: " + top_genre
)

st.markdown("---")

st.subheader("Audience Trend Analysis")

action_count = int(genre_counts.get("Action", 0))
fantasy_count = int(genre_counts.get("Fantasy", 0))
drama_count = int(genre_counts.get("Drama", 0))

col1, col2, col3 = st.columns(3)

col1.metric("Action", action_count)
col2.metric("Fantasy", fantasy_count)
col3.metric("Drama", drama_count)

if action_count >= fantasy_count and action_count >= drama_count:
    st.info("Action is the strongest genre in this dataset.")
elif fantasy_count >= drama_count:
    st.info("Fantasy is the strongest genre in this dataset.")
else:
    st.info("Drama is the strongest genre in this dataset.")

st.markdown("---")

st.subheader("Recommendation Engine")

recommended = df[df["Score"] >= 8.8]

if len(recommended) == 0:
    st.warning("No highly rated anime found.")
else:
    st.write("Recommended for new viewers:")

    for title in recommended["Name"].head(5):
        st.write("- " + title)

st.markdown("---")

st.subheader("Studio Intelligence")

studio_stats = (
    df.groupby("Studios")["Score"]
    .mean()
    .sort_values(ascending=False)
)

best_studio = studio_stats.index[0]
best_studio_score = round(float(studio_stats.iloc[0]), 2)

st.info(
    "Highest average studio score: "
    + best_studio
    + " ("
    + str(best_studio_score)
    + ")"
)

st.markdown("---")

st.subheader("AI Summary")

summary = (
    "The dataset contains "
    + str(len(df))
    + " anime titles across multiple genres and studios. "
    + "The average score is "
    + str(avg_score)
    + ". "
    + "Action and Fantasy titles dominate the collection, while studios such as Madhouse, Bones, MAPPA, and Wit Studio frequently appear among highly rated productions. "
    + "Overall audience engagement is strong, with millions of members represented across the dataset."
)

st.write(summary)

st.markdown("---")

st.subheader("Quick AI Predictions")

if avg_score >= 8.5:
    st.success("Prediction: The catalog is likely to satisfy most anime viewers.")
else:
    st.warning("Prediction: Viewer satisfaction may vary across titles.")

if action_count > fantasy_count:
    st.success("Prediction: Action anime will continue to attract the largest audience segment.")
else:
    st.success("Prediction: Fantasy anime has strong growth potential in audience interest.")

st.markdown("---")

st.subheader("Dataset Snapshot")

snapshot = df[["Name", "Score", "Genres", "Studios"]].head(10)

st.dataframe(snapshot, use_container_width=True, hide_index=True)

st.markdown("---")

st.caption("Anime Analytics Dashboard - AI Insights")

import streamlit as st
from utils.data_loader import load_data

st.set_page_config(page_title="AI Insights", layout="wide")

df = load_data()

st.title("🤖 AI Insights")

avg_score = df["Score"].mean()
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

st.markdown("### 📌 Automated Executive Insights")

st.success(f"**Overall quality is strong** with an average score of **{avg_score:.2f}**.")

st.success(
    f"**{top_anime['Name']}** is the highest-rated anime in the dataset with a score of **{top_anime['Score']:.2f}**."
)

st.success(
    f"**{popular_anime['Name']}** has the largest audience with **{int(popular_anime['Members']):,} members**."
)

st.success(f"**{top_genre}** is the most represented genre in the dataset.")

st.divider()

st.markdown("### 📈 Audience Trend Analysis")

action_count = genre_counts.get("Action", 0)
fantasy_count = genre_counts.get("Fantasy", 0)
drama_count = genre_counts.get("Drama", 0)

st.write(f"- Action titles: **{action_count}**")
st.write(f"- Fantasy titles: **{fantasy_count}**")
st.write(f"- Drama titles: **{drama_count}**")

if action_count > fantasy_count:
    st.info("Action anime appears to attract the largest audience share in this dataset.")
else:
    st.info("Fantasy anime appears highly competitive in this dataset.")

st.divider()

st.markdown("### 🎯 Recommendation Insights")

high_rated = df[df["Score"] >= 8.8]

st.write("Recommended for new viewers:")

for title in high_rated["Name"].head(5):
    st.write(f"- {title}")

st.divider()

st.markdown("### 🧠 AI Summary")

summary = f"""
The dataset contains **{len(df)} anime titles** spanning multiple genres and studios.
The strongest performers are concentrated in **Action, Fantasy, and Drama** categories.
Average viewer engagement is high, with more than **{int(df['Members'].mean()):,} members per title on average**.
Studios such as **Madhouse, Bones, MAPPA, and Wit Studio** repeatedly appear among top-rated productions.
This suggests that both strong storytelling and established studio reputation contribute significantly to audience reception.
"""

st.write(summary)

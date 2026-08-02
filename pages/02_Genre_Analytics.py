import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

# ---------------------------------------------------

# PAGE CONFIG

# ---------------------------------------------------

st.set_page_config(
page_title="Genre Analytics",
page_icon="🎭",
layout="wide"
)

# ---------------------------------------------------

# LOAD DATA

# ---------------------------------------------------

df = load_data()

# Safety check

if df.empty:
st.error("Dataset is empty. Please check data/anime_dataset.csv")
st.stop()

# ---------------------------------------------------

# PAGE HEADER

# ---------------------------------------------------

st.title("🎭 Genre Analytics")
st.markdown(
"Analyze genre popularity, average ratings, and genre-wise anime distribution."
)

st.divider()

# ---------------------------------------------------

# PREPARE GENRE DATA

# ---------------------------------------------------

genre_series = (
df["Genres"]
.dropna()
.str.split(",")
.explode()
.str.strip()
)

genre_counts = genre_series.value_counts().reset_index()
genre_counts.columns = ["Genre", "Count"]

# ---------------------------------------------------

# TOP GENRES CHART

# ---------------------------------------------------

st.subheader("🔥 Top Genres by Anime Count")

fig = px.bar(
genre_counts.head(15),
x="Genre",
y="Count",
text="Count",
color="Count",
color_continuous_scale="Blues",
template="plotly_dark"
)

fig.update_layout(
title="Top 15 Genres",
title_x=0.5,
xaxis_title="Genre",
yaxis_title="Number of Anime"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------

# AVERAGE SCORE BY GENRE

# ---------------------------------------------------

st.subheader("⭐ Average Score by Genre")

rows = []

for _, row in df.iterrows():
genres = str(row["Genres"]).split(",")

```
for g in genres:
    rows.append([g.strip(), row["Score"]])
```

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
text_auto=".2f",
color="Score",
color_continuous_scale="Viridis",
template="plotly_dark"
)

fig2.update_layout(
title="Highest Rated Genres",
title_x=0.5,
xaxis_title="Genre",
yaxis_title="Average Score"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------------------------------------------

# GENRE FILTER

# ---------------------------------------------------

st.subheader("🔎 Explore Anime by Genre")

selected_genre = st.selectbox(
"Select a Genre",
sorted(genre_counts["Genre"].unique())
)

filtered = df[
df["Genres"].str.contains(selected_genre, case=False, na=False)
]

st.write(f"**Total anime found:** {len(filtered)}")

st.dataframe(
filtered[["Name", "Score", "Genres", "Studios", "Members"]],
use_container_width=True,
hide_index=True
)

st.divider()

# ---------------------------------------------------

# TOP TITLES IN SELECTED GENRE

# ---------------------------------------------------

st.subheader(f"🏆 Top Rated {selected_genre} Anime")

top_genre_anime = (
filtered.sort_values("Score", ascending=False)
[["Name", "Score", "Studios"]]
.head(10)
)

st.dataframe(
top_genre_anime,
use_container_width=True,
hide_index=True
)

st.divider()

# ---------------------------------------------------

# QUICK INSIGHTS

# ---------------------------------------------------

st.subheader("🧠 Genre Insights")

top_genre = genre_counts.iloc[0]["Genre"]
top_genre_count = int(genre_counts.iloc[0]["Count"])

highest_rated_genre = avg_score.iloc[0]["Genre"]
highest_rated_score = float(avg_score.iloc[0]["Score"])

col1, col2 = st.columns(2)

with col1:
st.success(
f"**Most Popular Genre:** {top_genre} ({top_genre_count} anime)"
)

with col2:
st.success(
f"**Highest Rated Genre:** {highest_rated_genre} ({highest_rated_score:.2f})"
)

st.info(
"Genres with both high popularity and high average score are often strong entry points for new anime viewers."
)

st.divider()

# ---------------------------------------------------

# FOOTER

# ---------------------------------------------------

st.markdown(
"""
--- <center> <b>Genre Analytics</b><br>
Built with ❤️ using Streamlit & Plotly </center>
""",
unsafe_allow_html=True
)

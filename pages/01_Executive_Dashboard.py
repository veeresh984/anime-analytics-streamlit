import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.charts import (
rating_histogram,
top_genres_chart,
score_popularity_scatter,
)
from utils.insights import generate_executive_insights

# ---------------------------------------------------

# PAGE CONFIG

# ---------------------------------------------------

st.set_page_config(
page_title="Executive Dashboard",
page_icon="📊",
layout="wide",
)

# ---------------------------------------------------

# LOAD DATA

# ---------------------------------------------------

df = load_data()

# Safety check

if df.empty:
st.error("Dataset is empty. Please check data/anime_dataset.csv")
st.stop()

# Ensure numeric columns

for col in ["Score", "Members", "Popularity"]:
if col in df.columns:
df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------------------------------------------

# PAGE HEADER

# ---------------------------------------------------

st.title("📊 Executive Dashboard")
st.markdown(
"Comprehensive overview of anime ratings, popularity, genres, and audience engagement."
)

st.divider()

# ---------------------------------------------------

# KPI METRICS

# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
st.metric(
"🎬 Total Anime",
f"{len(df):,}",
)

with col2:
st.metric(
"⭐ Average Score",
f"{df['Score'].mean():.2f}",
)

with col3:
st.metric(
"👥 Total Members",
f"{int(df['Members'].sum()):,}",
)

with col4:
st.metric(
"🏢 Total Studios",
f"{df['Studios'].nunique():,}",
)

st.divider()

# ---------------------------------------------------

# CHARTS ROW 1

# ---------------------------------------------------

left, right = st.columns(2)

with left:
st.subheader("⭐ Score Distribution")
fig_hist = rating_histogram(df)
st.plotly_chart(fig_hist, use_container_width=True)

with right:
st.subheader("🎭 Top Genres")
fig_genre = top_genres_chart(df)
st.plotly_chart(fig_genre, use_container_width=True)

st.divider()

# ---------------------------------------------------

# CHARTS ROW 2

# ---------------------------------------------------

st.subheader("📈 Score vs Popularity")

fig_scatter = score_popularity_scatter(df)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ---------------------------------------------------

# TOP ANIME TABLE

# ---------------------------------------------------

st.subheader("🏆 Top Rated Anime")

top_anime = (
df.sort_values("Score", ascending=False)
[["Name", "Score", "Genres", "Studios", "Members"]]
.head(15)
)

st.dataframe(
top_anime,
use_container_width=True,
hide_index=True,
)

st.divider()

# ---------------------------------------------------

# QUICK INSIGHTS

# ---------------------------------------------------

st.subheader("🧠 Automated Insights")

insights = generate_executive_insights(df)

for insight in insights:
st.info(insight)

st.divider()

# ---------------------------------------------------

# QUICK STATS

# ---------------------------------------------------

st.subheader("📌 Quick Statistics")

s1, s2, s3 = st.columns(3)

# Highest rated

highest = df.sort_values("Score", ascending=False).iloc[0]

with s1:
st.success(
f"**Highest Rated:** {highest['Name']} ({highest['Score']:.2f})"
)

# Most popular

popular = df.sort_values("Members", ascending=False).iloc[0]

with s2:
st.success(
f"**Most Popular:** {popular['Name']}"
)

# Most common genre

genre_counts = (
df["Genres"]
.dropna()
.str.split(",")
.explode()
.str.strip()
.value_counts()
)

with s3:
st.success(
f"**Top Genre:** {genre_counts.index[0]}"
)

st.divider()

# ---------------------------------------------------

# DATA PREVIEW

# ---------------------------------------------------

st.subheader("📄 Dataset Preview")

st.dataframe(
df.head(10),
use_container_width=True,
hide_index=True,
)

st.caption(
f"Showing first 10 rows out of {len(df):,} records."
)

st.divider()

# ---------------------------------------------------

# FOOTER

# ---------------------------------------------------

st.markdown(
"""
--- <center> <b>Anime Analytics Dashboard</b><br>
Built with ❤️ using Streamlit & Plotly </center>
""",
unsafe_allow_html=True,
)

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

# Page configuration

st.set_page_config(
page_title="Rating Insights",
layout="wide"
)

# Load dataset

df = load_data()

# Stop if dataset is empty

if df.empty:
st.error("Dataset is empty. Please check data/anime_dataset.csv")
st.stop()

# Convert Score column to numeric

df["Score"] = pd.to_numeric(df["Score"], errors="coerce")

# Remove missing values

df = df.dropna(subset=["Score"])

# Title

st.title("Rating Insights")
st.write("Explore anime rating distribution and statistics.")

# Divider

st.divider()

# Histogram

st.subheader("Score Distribution")

fig_hist = px.histogram(
df,
x="Score",
nbins=15,
title="Anime Score Distribution"
)

st.plotly_chart(fig_hist, use_container_width=True)

# Divider

st.divider()

# Box plot

st.subheader("Box Plot of Scores")

fig_box = px.box(
df,
y="Score",
points="all"
)

st.plotly_chart(fig_box, use_container_width=True)

# Divider

st.divider()

# Statistics

st.subheader("Statistical Summary")

stats = df["Score"].describe().to_frame().T
st.dataframe(stats, use_container_width=True)

# Divider

st.divider()

# Quantiles

st.subheader("Quartile Analysis")

q1 = df["Score"].quantile(0.25)
median = df["Score"].median()
q3 = df["Score"].quantile(0.75)

col1, col2, col3 = st.columns(3)

col1.metric("Q1", f"{q1:.2f}")
col2.metric("Median", f"{median:.2f}")
col3.metric("Q3", f"{q3:.2f}")

# Divider

st.divider()

# Outlier detection

st.subheader("Outlier Anime")

iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

outliers = df[(df["Score"] < lower) | (df["Score"] > upper)]

if len(outliers) == 0:
st.success("No significant outliers found.")
else:
st.dataframe(
outliers[["Name", "Score", "Genres"]],
use_container_width=True,
hide_index=True
)

# Divider

st.divider()

# Top rated

st.subheader("Top Rated Anime")

top_rated = (
df.sort_values("Score", ascending=False)
[["Name", "Score", "Genres"]]
.head(10)
)

st.dataframe(
top_rated,
use_container_width=True,
hide_index=True
)

# Footer

st.divider()

st.caption("Anime Analytics Dashboard - Rating Insights")

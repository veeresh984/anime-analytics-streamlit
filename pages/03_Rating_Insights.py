03_Rating_Insights.py
import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Rating Insights", layout="wide")

df = load_data()

st.title("⭐ Rating Insights")

st.subheader("Score Distribution")

fig = px.histogram(
    df,
    x="Score",
    nbins=15,
    title="Distribution of Anime Scores",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Box Plot")

fig2 = px.box(df, y="Score", points="all")

st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Statistical Summary")

st.dataframe(df["Score"].describe().to_frame().T, use_container_width=True)

st.divider()

q1 = df["Score"].quantile(0.25)
q3 = df["Score"].quantile(0.75)
iqr = q3 - q1

outliers = df[
    (df["Score"] < q1 - 1.5 * iqr) |
    (df["Score"] > q3 + 1.5 * iqr)
]

st.subheader("Outlier Anime")

if len(outliers) == 0:
    st.success("No significant outliers found.")
else:
    st.dataframe(
        outliers[["Name", "Score", "Genres"]],
        use_container_width=True,
        hide_index=True,
    )

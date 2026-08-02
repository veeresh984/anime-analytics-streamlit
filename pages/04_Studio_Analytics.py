import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Studio Analytics", layout="wide")

df = load_data()

st.title("🏢 Studio Analytics")

studio_counts = df["Studios"].value_counts().reset_index()
studio_counts.columns = ["Studio", "Anime_Count"]

st.subheader("Top Studios by Production Count")

fig = px.bar(
    studio_counts.head(15),
    x="Studio",
    y="Anime_Count",
    text="Anime_Count",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Average Score by Studio")

avg_score = (
    df.groupby("Studios")["Score"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig2 = px.bar(
    avg_score.head(15),
    x="Studios",
    y="Score",
    text_auto=".2f",
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

selected_studio = st.selectbox(
    "Select Studio",
    sorted(df["Studios"].unique()),
)

studio_df = df[df["Studios"] == selected_studio]

st.subheader(f"Anime by {selected_studio}")

st.dataframe(
    studio_df[["Name", "Score", "Genres", "Members"]],
    use_container_width=True,
    hide_index=True,
)

import streamlit as st
import pandas as pd
from utils.data_loader import load_data

st.set_page_config(page_title="Synopsis Explorer", layout="wide")

df = load_data()

if df.empty:
    st.error("Dataset is empty. Please check data/anime_dataset.csv")
    st.stop()

st.title("Synopsis Explorer")
st.write("Search anime titles and explore their synopsis, genres, studio, and audience data.")

st.markdown("---")

anime_names = sorted(df["Name"].dropna().unique())

selected_anime = st.selectbox(
    "Select an Anime",
    anime_names
)

anime = df[df["Name"] == selected_anime].iloc[0]

st.subheader(selected_anime)

col1, col2, col3 = st.columns(3)

col1.metric("Score", round(float(anime["Score"]), 2))
col2.metric("Popularity", int(anime["Popularity"]))
col3.metric("Members", f"{int(anime["Members"]):,}")

st.markdown("---")

st.write("**Genres**")
st.write(anime["Genres"])

st.write("**Studio**")
st.write(anime["Studios"])

st.markdown("---")

st.subheader("Synopsis")
st.write(anime["Synopsis"])

st.markdown("---")

st.subheader("Quick Summary")

summary = (
    selected_anime
    + " is a "
    + str(anime["Genres"])
    + " anime produced by "
    + str(anime["Studios"])
    + ". It has a score of "
    + str(round(float(anime["Score"]), 2))
    + " and approximately "
    + f"{int(anime["Members"]):,}"
    + " members."
)

st.info(summary)

st.markdown("---")

st.subheader("Similar Anime")

first_genre = str(anime["Genres"]).split(",")[0].strip()

similar = df[
    df["Genres"].str.contains(first_genre, case=False, na=False)
]

similar = similar[similar["Name"] != selected_anime]

similar = similar.sort_values("Score", ascending=False).head(10)

if len(similar) == 0:
    st.warning("No similar anime found.")
else:
    st.dataframe(
        similar[["Name", "Score", "Genres", "Studios"]],
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")

st.subheader("Search by Keyword")

keyword = st.text_input("Enter a keyword from the synopsis")

if keyword:
    results = df[
        df["Synopsis"].str.contains(keyword, case=False, na=False)
    ]

    st.write("Results found:", len(results))

    if len(results) > 0:
        st.dataframe(
            results[["Name", "Score", "Genres"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No anime matched the keyword.")

st.markdown("---")

st.subheader("Dataset Preview")

st.dataframe(
    df[["Name", "Score", "Genres"]].head(10),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

st.caption("Anime Analytics Dashboard - Synopsis Explorer")

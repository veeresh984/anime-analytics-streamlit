import streamlit as st
from utils.data_loader import load_data

st.set_page_config(page_title="Synopsis Explorer", layout="wide")

df = load_data()

st.title("📖 Synopsis Explorer")

anime_names = sorted(df["Name"].tolist())

selected = st.selectbox("Search Anime", anime_names)

anime = df[df["Name"] == selected].iloc[0]

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Score", anime["Score"])
    st.metric("Popularity", anime["Popularity"])
    st.metric("Members", f"{int(anime['Members']):,}")

with col2:
    st.write(f"**Genres:** {anime['Genres']}")
    st.write(f"**Studio:** {anime['Studios']}")

st.divider()

st.subheader("Synopsis")
st.write(anime["Synopsis"])

st.divider()

st.subheader("Similar Anime (Same Genre)")

first_genre = str(anime["Genres"]).split(",")[0].strip()

similar = df[
    df["Genres"].str.contains(first_genre, na=False) &
    (df["Name"] != selected)
].sort_values("Score", ascending=False).head(10)

st.dataframe(
    similar[["Name", "Score", "Genres"]],
    use_container_width=True,
    hide_index=True,
)

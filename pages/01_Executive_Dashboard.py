import streamlit as st
from utils.data_loader import load_data
from utils.charts import rating_histogram, top_genres_chart, score_popularity_scatter

st.set_page_config(page_title="Executive Dashboard", layout="wide")

df = load_data()

st.title("📊 Executive Dashboard")
st.markdown("High-level overview of the anime dataset.")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Anime", len(df))
col2.metric("Average Score", f"{df['Score'].mean():.2f}")
col3.metric("Total Members", f"{int(df['Members'].sum()):,}")
col4.metric("Total Studios", df['Studios'].nunique())

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.subheader("⭐ Score Distribution")
    st.plotly_chart(rating_histogram(df), use_container_width=True)

with c2:
    st.subheader("🎭 Top Genres")
    st.plotly_chart(top_genres_chart(df), use_container_width=True)

st.divider()

st.subheader("📈 Score vs Popularity")
st.plotly_chart(score_popularity_scatter(df), use_container_width=True)

st.divider()

st.subheader("🏆 Top Rated Anime")
top_df = df.sort_values("Score", ascending=False)[
    ["Name", "Score", "Genres", "Studios"]
].head(15)

st.dataframe(top_df, use_container_width=True, hide_index=True)
```

---

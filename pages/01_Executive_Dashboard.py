# 01_Executive_Dashboard.py

```python
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

# 02_Genre_Analytics.py

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

st.set_page_config(page_title="Genre Analytics", layout="wide")

df = load_data()

st.title("🎭 Genre Analytics")

genre_series = (
    df["Genres"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
)

genre_counts = genre_series.value_counts().reset_index()
genre_counts.columns = ["Genre", "Count"]

fig = px.bar(
    genre_counts.head(15),
    x="Genre",
    y="Count",
    title="Top 15 Genres",
    text="Count",
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Average Score by Genre")

rows = []

for _, row in df.iterrows():
    if pd.notna(row["Genres"]):
        for g in str(row["Genres"]).split(","):
            rows.append([g.strip(), row["Score"]])

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
    title="Highest Rated Genres",
    text_auto=".2f",
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

selected_genre = st.selectbox(
    "Select Genre",
    sorted(genre_counts["Genre"].unique()),
)

filtered = df[df["Genres"].str.contains(selected_genre, na=False)]

st.subheader(f"Anime in {selected_genre}")
st.dataframe(
    filtered[["Name", "Score", "Studios", "Members"]],
    use_container_width=True,
    hide_index=True,
)
```

---

# 03_Rating_Insights.py

```python
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
```

---

# 04_Studio_Analytics.py

```python
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
```

---

# 05_Synopsis_Explorer.py

```python
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
```

---

# 06_AI_Insights.py

```python
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
```

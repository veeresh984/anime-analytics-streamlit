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
    page_title="Anime Analytics Dashboard",
    page_icon="🎌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #31333f;
    }
    .title-text {
        font-size: 42px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0px;
    }
    .subtitle-text {
        font-size: 18px;
        color: #b0b3b8;
        margin-top: -10px;
    }
    .insight-box {
        background-color: #1c1f26;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #ff4b4b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = load_data()

# Ensure numeric columns
numeric_cols = ["Score", "Members", "Popularity"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown('<p class="title-text">🎌 Anime Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle-text">Deep analytics and insights for top anime TV shows</p>',
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("🔎 Filters")

# Genre filter
all_genres = sorted(
    list(
        set(
            g.strip()
            for genres in df["Genres"].dropna()
            for g in str(genres).split(",")
        )
    )
)

selected_genres = st.sidebar.multiselect(
    "Select Genre(s)",
    options=all_genres,
    default=[],
)

# Score filter
min_score = float(df["Score"].min())
max_score = float(df["Score"].max())

score_range = st.sidebar.slider(
    "Score Range",
    min_value=round(min_score, 1),
    max_value=round(max_score, 1),
    value=(round(min_score, 1), round(max_score, 1)),
)

# Apply filters
filtered_df = df.copy()

if selected_genres:
    filtered_df = filtered_df[
        filtered_df["Genres"].apply(
            lambda x: any(g in str(x) for g in selected_genres)
        )
    ]

filtered_df = filtered_df[
    (filtered_df["Score"] >= score_range[0])
    & (filtered_df["Score"] <= score_range[1])
]

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.subheader("📊 Executive Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Anime", f"{len(filtered_df):,}")

with col2:
    avg_score = filtered_df["Score"].mean()
    st.metric("Average Score", f"{avg_score:.2f}")

with col3:
    total_members = int(filtered_df["Members"].sum())
    st.metric("Total Members", f"{total_members:,}")

with col4:
    total_studios = filtered_df["Studios"].nunique()
    st.metric("Total Studios", f"{total_studios:,}")

st.divider()

# ---------------------------------------------------
# CHARTS
# ---------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⭐ Score Distribution")
    fig_hist = rating_histogram(filtered_df)
    st.plotly_chart(fig_hist, use_container_width=True)

with col_right:
    st.subheader("🎭 Top Genres")
    fig_genres = top_genres_chart(filtered_df)
    st.plotly_chart(fig_genres, use_container_width=True)

st.divider()

# Scatter plot
st.subheader("📈 Score vs Popularity")
fig_scatter = score_popularity_scatter(filtered_df)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ---------------------------------------------------
# TOP ANIME TABLE
# ---------------------------------------------------
st.subheader("🏆 Top Rated Anime")

top_anime = (
    filtered_df.sort_values("Score", ascending=False)
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
# INSIGHTS
# ---------------------------------------------------
st.subheader("🧠 Automated Insights")

insights = generate_executive_insights(filtered_df)

st.markdown('<div class="insight-box">', unsafe_allow_html=True)

for item in insights:
    st.markdown(f"- {item}")

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------
# QUICK STATISTICS
# ---------------------------------------------------
st.subheader("📌 Quick Statistics")

stats_col1, stats_col2, stats_col3 = st.columns(3)

with stats_col1:
    st.write("**Highest Rated Anime**")
    top_title = filtered_df.sort_values("Score", ascending=False).iloc[0]
    st.success(f"{top_title['Name']} ({top_title['Score']:.2f})")

with stats_col2:
    st.write("**Most Popular Anime**")
    popular_title = filtered_df.sort_values("Members", ascending=False).iloc[0]
    st.success(f"{popular_title['Name']}")

with stats_col3:
    st.write("**Most Common Genre**")
    genre_counts = (
        filtered_df["Genres"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
    )
    st.success(genre_counts.index[0])

st.divider()

# ---------------------------------------------------
# NAVIGATION HELP
# ---------------------------------------------------
st.subheader("📂 Explore More Analytics")

st.info(
    """
    Use the **left sidebar navigation** to explore advanced analytics pages:

    - **Genre Analytics**
    - **Rating Insights**
    - **Studio Analytics**
    - **Synopsis Explorer**
    - **AI Insights**
    """
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown(
    """
    <hr>
    <center>
        Built with ❤️ using Streamlit & Plotly
    </center>
    """,
    unsafe_allow_html=True,
)

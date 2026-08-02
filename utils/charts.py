import pandas as pd
import plotly.express as px


def rating_histogram(df):
    fig = px.histogram(
        df,
        x="Score",
        nbins=15,
        title="Anime Score Distribution",
        template="plotly_dark",
    )

    fig.update_layout(
        xaxis_title="Score",
        yaxis_title="Count",
        title_x=0.5,
    )

    return fig


def top_genres_chart(df, top_n=10):
    genre_counts = (
        df["Genres"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    genre_counts.columns = ["Genre", "Count"]

    fig = px.bar(
        genre_counts,
        x="Genre",
        y="Count",
        text="Count",
        title=f"Top {top_n} Genres",
        template="plotly_dark",
    )

    fig.update_layout(title_x=0.5)

    return fig


def score_popularity_scatter(df):
    fig = px.scatter(
        df,
        x="Popularity",
        y="Score",
        size="Members",
        hover_name="Name",
        color="Score",
        color_continuous_scale="Turbo",
        title="Score vs Popularity",
        template="plotly_dark",
    )

    fig.update_layout(title_x=0.5)

    return fig


def studio_bar_chart(df, top_n=10):
    studio_counts = (
        df["Studios"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    studio_counts.columns = ["Studio", "Count"]

    fig = px.bar(
        studio_counts,
        x="Studio",
        y="Count",
        text="Count",
        title=f"Top {top_n} Studios",
        template="plotly_dark",
    )

    fig.update_layout(title_x=0.5)

    return fig


def average_score_by_genre(df, top_n=10):
    rows = []

    for _, row in df.iterrows():
        if pd.notna(row["Genres"]):
            for genre in str(row["Genres"]).split(","):
                rows.append([genre.strip(), row["Score"]])

    genre_df = pd.DataFrame(rows, columns=["Genre", "Score"])

    avg_scores = (
        genre_df.groupby("Genre")["Score"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig = px.bar(
        avg_scores,
        x="Genre",
        y="Score",
        text_auto=".2f",
        title=f"Top {top_n} Genres by Average Score",
        template="plotly_dark",
    )

    fig.update_layout(title_x=0.5)

    return fig

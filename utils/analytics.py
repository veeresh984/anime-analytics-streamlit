import pandas as pd


def dataset_summary(df):
    return {
        "total_anime": len(df),
        "average_score": round(df["Score"].mean(), 2),
        "total_members": int(df["Members"].sum()),
        "total_studios": df["Studios"].nunique(),
        "highest_score": round(df["Score"].max(), 2),
        "lowest_score": round(df["Score"].min(), 2),
    }


def top_rated(df, n=10):
    return (
        df.sort_values("Score", ascending=False)
        [["Name", "Score", "Genres", "Studios"]]
        .head(n)
    )


def most_popular(df, n=10):
    return (
        df.sort_values("Members", ascending=False)
        [["Name", "Members", "Score"]]
        .head(n)
    )


def genre_statistics(df):
    genre_series = (
        df["Genres"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
    )

    return genre_series.value_counts().reset_index(name="Count")


def studio_statistics(df):
    return (
        df.groupby("Studios")
        .agg(
            Anime_Count=("Name", "count"),
            Average_Score=("Score", "mean"),
        )
        .sort_values("Anime_Count", ascending=False)
        .reset_index()
    )


def score_quantiles(df):
    return {
        "q1": round(df["Score"].quantile(0.25), 2),
        "median": round(df["Score"].median(), 2),
        "q3": round(df["Score"].quantile(0.75), 2),
    }


def detect_outliers(df):
    q1 = df["Score"].quantile(0.25)
    q3 = df["Score"].quantile(0.75)
    iqr = q3 - q1

    outliers = df[
        (df["Score"] < q1 - 1.5 * iqr)
        | (df["Score"] > q3 + 1.5 * iqr)
    ]

    return outliers

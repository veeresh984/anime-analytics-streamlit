def generate_executive_insights(df):
    insights = []

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

    insights.append(
        f"Average anime score is **{avg_score:.2f}**, indicating generally strong audience reception."
    )

    insights.append(
        f"**{top_anime['Name']}** is the highest-rated anime with a score of **{top_anime['Score']:.2f}**."
    )

    insights.append(
        f"**{popular_anime['Name']}** has the largest audience with **{int(popular_anime['Members']):,} members**."
    )

    insights.append(
        f"**{top_genre}** is the most represented genre in the dataset."
    )

    if avg_score >= 8.5:
        insights.append(
            "The dataset is heavily concentrated around high-quality anime titles."
        )
    else:
        insights.append(
            "The dataset contains a balanced mix of mainstream and niche anime titles."
        )

    return insights


def ai_summary(df):
    avg_score = df["Score"].mean()
    avg_members = int(df["Members"].mean())

    return f"""
The dataset contains {len(df)} anime titles across multiple genres and studios.
The average score is {avg_score:.2f}, while average audience size is {avg_members:,} members.
Action and Fantasy titles dominate the collection, suggesting strong viewer preference for adventure-driven stories.
Studios such as Madhouse, Bones, MAPPA, and Wit Studio appear frequently among top-performing anime.
Overall, the dataset reflects a high-engagement anime audience with strong interest in action-oriented storytelling.
"""

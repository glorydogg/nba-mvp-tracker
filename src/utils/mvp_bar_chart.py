import matplotlib.pyplot as plt


def plot_mvp_bar_chart(df):
    top_df = df.head(10)

    plt.figure(figsize=(10,6))
    plt.bar(top_df["PLAYER_NAME"], top_df["MVP_SCORE"])

    plt.title("Top MVP Scores")
    plt.ylabel("Player")
    plt.xlabel("MVP Scores")

    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()




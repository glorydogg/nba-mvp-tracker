import logging
import datetime
import uuid
from api.api_client import NBAClient
from data_processing.cleaning import cleaning_player_stats
from models.mvp_scoring import compute_mvp_score 
from models.mvp_scoring import stat_contributions
from utils.mvp_bar_chart import plot_mvp_bar_chart
from utils.db import create_table, insert_players_batch
from utils.io_utils import NBALogger 
from utils.aws_uploader import S3Uploader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def run_pipline():
    create_table()
    run_id = str(uuid.uuid4())
    
    client = NBAClient("2025-26")
    raw_df = client.get_all_player_stats()

    if raw_df is None or raw_df.empty:
        print("API returned no data. Pipeline stopped.")
        return

    clean_df = cleaning_player_stats(raw_df)

    ranked_df = compute_mvp_score(clean_df)
    final_df = stat_contributions(ranked_df)
    final_df["MVP_SCORE"] = final_df["MVP_SCORE"].round(2)
    
    print(final_df.head(10))
    # plot_mvp_bar_chart(final_df)

    mvp_log = NBALogger()
    mvp_log.log_top_ten(ranked_df)
    
    date = datetime.datetime.today()
    print("INSERTING TOP 10 WITH RUN_DATE: ", date)

    # Build tuple list for single batch insertion
    top_10_df = final_df.head(10)
    batch_data = [
        (run_id, row["PLAYER_NAME"], float(row["MVP_SCORE"]), str(date))
        for _, row in top_10_df.iterrows()
    ]

    # Insert all 10 players in one database call
    insert_players_batch(batch_data)
    print("Batch insertion into Snowflake complete!")

    uploader = S3Uploader()
    uploader.upload("data/top_ten_mvp.csv", f"rankings/{date.strftime('%Y-%m-%d_%H-%M')}_top_ten_mvp.csv")

if __name__ == "__main__":
    run_pipline()
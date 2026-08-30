import logging
import datetime
import uuid
import sys
from pathlib import Path

# Ensure the src package is importable when running `python src/main.py`
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from api.api_client import NBAClient
from data_processing.cleaning import cleaning_player_stats
from models.mvp_scoring import compute_mvp_score, stat_contributions
from utils.mvp_bar_chart import plot_mvp_bar_chart
from utils.db import create_table, insert_players_batch
from utils.io_utils import NBALogger
from utils.aws_uploader import S3Uploader

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def run_pipeline(season: str = "2025-26", upload_to_s3: bool = True, show_chart: bool = False):
    """Main MVP ranking pipeline."""
    create_table()
    run_id = str(uuid.uuid4())

    client = NBAClient(season)
    raw_df = client.get_all_player_stats()

    if raw_df is None or raw_df.empty:
        logger.error("API returned no data. Pipeline stopped.")
        return

    clean_df = cleaning_player_stats(raw_df)
    ranked_df = compute_mvp_score(clean_df)
    final_df = stat_contributions(ranked_df)
    final_df["MVP_SCORE"] = final_df["MVP_SCORE"].round(2)

    print("\n--- Top 10 MVP Candidates ---")
    print(final_df[["PLAYER_NAME", "MVP_SCORE"]].head(10).to_string(index=False))
    print("-----------------------------\n")

    if show_chart:
        plot_mvp_bar_chart(final_df)

    # Local CSV log
    mvp_log = NBALogger()
    mvp_log.log_top_ten(ranked_df)

    # Prepare batch insert
    run_date = datetime.datetime.now()
    top_10_df = final_df.head(10)
    batch_data = [
        (run_id, row["PLAYER_NAME"], float(row["MVP_SCORE"]), run_date)
        for _, row in top_10_df.iterrows()
    ]

    insert_players_batch(batch_data)
    logger.info("Batch insertion into Snowflake complete.")

    if upload_to_s3:
        try:
            uploader = S3Uploader()
            local_csv = "data/top_ten_mvp.csv"
            s3_key = f"rankings/{run_date.strftime('%Y-%m-%d_%H-%M')}_top_ten_mvp.csv"
            uploader.upload(local_csv, s3_key)
        except Exception as e:
            logger.warning(f"S3 upload skipped or failed: {e}")


if __name__ == "__main__":
    run_pipeline()
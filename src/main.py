import logging
from api.api_client import NBAClient
from data_processing.cleaning import cleaning_player_stats
from models.mvp_scoring import compute_mvp_score 
from models.mvp_scoring import stat_contributions
from utils.mvp_bar_chart import plot_mvp_bar_chart
from utils.io_utils import NBALogger 
from utils.aws_uploader import S3Uploader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def run_pipline():
    
    client = NBAClient("2025-26")
    raw_df = client.get_all_player_stats()

    clean_df = cleaning_player_stats(raw_df)

    ranked_df = compute_mvp_score(clean_df)
    final_df = stat_contributions(ranked_df)
    final_df["MVP_SCORE"] = final_df["MVP_SCORE"].round(2)
    
    print(final_df.head(10))
    plot_mvp_bar_chart(final_df)

   
    mvp_log = NBALogger()
    mvp_log.log_top_ten(ranked_df)

    uploader = S3Uploader()
    uploader.upload("data/top_ten_mvp.csv", "rankings/top_ten_mvp.csv")

if __name__ == "__main__":
    run_pipline()
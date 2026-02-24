import logging
import datetime
import uuid
from api.api_client import NBAClient
from data_processing.cleaning import cleaning_player_stats
from models.mvp_scoring import compute_mvp_score 
from models.mvp_scoring import stat_contributions
from utils.mvp_bar_chart import plot_mvp_bar_chart
from utils.db import create_table, insert_player
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
        print("Api returned no data. Pipeline stopped.")
        return

    clean_df = cleaning_player_stats(raw_df)

    ranked_df = compute_mvp_score(clean_df)
    final_df = stat_contributions(ranked_df)
    final_df["MVP_SCORE"] = final_df["MVP_SCORE"].round(2)
    
    print(final_df.head(10))
    #plot_mvp_bar_chart(final_df)

   
    mvp_log = NBALogger()
    mvp_log.log_top_ten(ranked_df)
    
    date = datetime.datetime.today()
    print("INSERTING TOP 10 WITH RUN_DATE: ", date)
    for rank, (_, row) in enumerate(final_df.head(10).iterrows(), start=1):

        name = row["PLAYER_NAME"]
        score = row["MVP_SCORE"]
        run_date = date
        
        print("Inserting: ", name, score)
        insert_player(run_id, name, score, run_date)
    
        

    uploader = S3Uploader()
    uploader.upload("data/top_ten_mvp.csv", "rankings/top_ten_mvp.csv")

if __name__ == "__main__":
    run_pipline()
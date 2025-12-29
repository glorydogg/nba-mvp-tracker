import pandas as pd 
import os
import logging


logger = logging.getLogger(__name__)


class NBALogger:
    def __init__(self, filename= "top_ten_mvp.csv"):
        self.directory = "data"
        self.filename = filename
        self.filepath = os.path.join(self.directory, self.filename)

    
    def log_top_ten(self, df: pd.DataFrame):
        """ Saves top 10 players to csv """

        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)

            # Get top 10
            top_ten = df.head(10)

            # Save to csv
            top_ten.to_csv(self.filepath, index=False)

            print(f"Successfully saved logged top 10 players to {self.filepath}") 

            print("\n--- Current MVP Leaders ---")
            print(top_ten[['PLAYER_NAME', 'MVP_SCORE']].to_string(index=False))
            print("---------------------")
        except Exception as e:
            logger.error(f"Failed to log top ten locally: {e}")

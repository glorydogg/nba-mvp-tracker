import logging
import time
import pandas as pd
from nba_api.stats.endpoints import LeagueDashPlayerStats

logger = logging.getLogger(__name__)


class NBAClient:
    def __init__(self, season: str):
        self.season = season
        self.headers = {
            'Host': 'stats.nba.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.nba.com/',
            'Origin': 'https://www.nba.com',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
}


    def get_all_player_stats(self, retries=3) -> list:
        """ Calls nba api libary with reties"""

        logger.info(f"Fetching stats for {self.season} season")
        for i in range(retries):
            try:
                stats = LeagueDashPlayerStats(
                    season=self.season,
                    league_id_nullable='00',             
                    measure_type_detailed_defense='Base',
                    per_mode_detailed='PerGame',   # This will actually give you PPG/RPG directly!
                    timeout=59)
                df = stats.get_data_frames()[0]

                logger.info(f"Succesfully  retrieved data on attempt {i + 1}\n")
                return df
            except Exception as e:
                logger.warning(f"Attempt {i + 1} failed Retrying...")
                if i < retries - 1:
                    time.sleep(2)
    
        logger.error("All NBA API attempts failed")        
        return pd.DataFrame()



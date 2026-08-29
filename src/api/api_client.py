import logging
import time
import pandas as pd
from curl_cffi import requests as cr
from nba_api.stats.library.http import NBAStatsHTTP
from nba_api.stats.endpoints import LeagueDashPlayerStats

logger = logging.getLogger(__name__)

# --- FIX AKAMAI TLS FIREWALL ---
session = cr.Session(impersonate="chrome120")

# Warm up session on nba.com
try:
    session.get("https://www.nba.com/stats/", timeout=10)
except Exception:
    pass

NBAStatsHTTP.get_session = lambda self: session
# -------------------------------


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

    def get_all_player_stats(self, retries=3) -> pd.DataFrame:
        """Calls nba api library with retries."""
        logger.info(f"Fetching stats for {self.season} season")
        
        for i in range(retries):
            try:
                stats = LeagueDashPlayerStats(
                    season=self.season,
                    league_id_nullable='00',
                    measure_type_detailed_defense='Base',  # Correct parameter name
                    per_mode_detailed='PerGame',
                    headers=self.headers, 
                    timeout=20
                )
                
                df = stats.get_data_frames()[0]

                if df is not None and not df.empty:
                    logger.info(f"Successfully retrieved data on attempt {i + 1}\n")
                    return df
                    
            except Exception as e:
                logger.warning(f"Attempt {i + 1} failed ({e}). Retrying...")
                if i < retries - 1:
                    time.sleep(2)
    
        logger.error("All NBA API attempts failed")        
        return pd.DataFrame()
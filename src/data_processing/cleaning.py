import logging
import pandas as pd

logger = logging.getLogger(__name__)

def cleaning_player_stats(df):
    print(f"Total players received from API: {len(df)}")
    
    
    df["PPG"] = df["PTS"]
    df["RPG"] = df["REB"]
    df["APG"] = df["AST"]
    df["MPG"] = df["MIN"] 

    #  True Shooting % 
    df["TS_PCT"] = df["PTS"] / (2 * (df["FGA"] + 0.44 * df["FTA"]) + 1e-9)

    print(f"Actual Max MPG found: {df['MPG'].max()}") 

    # Apply Filters
    df = df[df["MPG"] >= 20]
    
    max_gp = df["GP"].max()
    required_gp = max_gp * 0.70
    df = df[df["GP"] >= required_gp]

    print(f"Players remaining after filters: {len(df)}")
    return df
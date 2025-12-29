import logging
import pandas as pd

logger = logging.getLogger(__name__)

def cleaning_player_stats(df):
    print(f"Total players received from API: {len(df)}")
    
    # 1. SINCE YOU ARE USING 'PerGame' MODE:
    # PTS is already PPG, REB is already RPG, and MIN is already MPG.
    df["PPG"] = df["PTS"]
    df["RPG"] = df["REB"]
    df["APG"] = df["AST"]
    df["MPG"] = df["MIN"] # Do NOT divide by GP here!

    # 2. True Shooting % (Calculated the same way)
    df["TS_PCT"] = df["PTS"] / (2 * (df["FGA"] + 0.44 * df["FTA"]) + 1e-9)

    print(f"Actual Max MPG found: {df['MPG'].max()}") # This should now say ~35-38

    # 3. Apply Filters
    df = df[df["MPG"] >= 20] # Now players like Jokic/Luka will pass this
    
    max_gp = df["GP"].max()
    required_gp = max_gp * 0.70
    df = df[df["GP"] >= required_gp]

    print(f"Players remaining after filters: {len(df)}")
    return df
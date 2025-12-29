import pandas as pd

WEIGHTS = {
    "PPG": .35,
    "TS_PCT": .15,
    "W_PCT": .20,
    "PLUS_MINUS": .20,
    "APG": .05,
    "RPG": .05
}


def normalize(df, columns):
    # adding z scores
    for col in columns:
        mean = df[col].mean()
        std = df[col].std()

        # avoid dividing by 0
        if std == 0:
            df[f"Z_{col}"] = 0
        else:
            df[f"Z_{col}"] = (df[col] - mean) / std

    return df

def compute_mvp_score(df):
    stats_to_normalize = ["PPG", "TS_PCT", "W_PCT", "PLUS_MINUS", "APG", "RPG"]
    df = normalize(df, stats_to_normalize)
    df["MVP_SCORE"] = (
        WEIGHTS["PPG"] * df["Z_PPG"] +   
        WEIGHTS["TS_PCT"] * df["Z_TS_PCT"] +
        WEIGHTS["W_PCT"] * df["Z_W_PCT"] +
        WEIGHTS["PLUS_MINUS"] * df["Z_PLUS_MINUS"] +
        WEIGHTS["APG"] * df["Z_APG"] +
        WEIGHTS["RPG"] * df["Z_RPG"]
    )
    
    #  best -> worst
    df = df.sort_values("MVP_SCORE", ascending=False)
    
    
    return df


def stat_contributions(df):
    for stat, weight in WEIGHTS.items():
        z_col = f"Z_{stat}"
        contrib_col = f"{stat}_C"
        df[contrib_col] = weight * df[z_col]
    return df

 
# NBA MVP Tracker

A Python analytics pipeline that ranks NBA players by MVP likelihood using a weighted z-score model.

Ingests live player stats from the NBA API, cleans and normalizes the data, computes composite MVP scores, and persists results to Snowflake with optional AWS S3 export.

## How It Works

Player stats are pulled from the NBA API and normalized using z-scores across 6 key metrics:

| Metric            | Weight |
|-------------------|--------|
| Points Per Game   | 35%    |
| Team Win %        | 20%    |
| Plus/Minus        | 20%    |
| True Shooting %   | 15%    |
| Assists Per Game  | 5%     |
| Rebounds Per Game | 5%     |

Rankings are stored in Snowflake and exported to CSV.

## Setup

1. Clone the repo
2. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
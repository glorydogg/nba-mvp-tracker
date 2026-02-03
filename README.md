# NBA MVP Tracker

A Python-based analytics pipeline that ranks NBA players using a weighted z-score model to estimate MVP performance.  
The project ingests player stats from an API, cleans and normalizes the data, computes composite MVP scores, visualizes results, and persists the top rankings in a SQLite database (with optional upload to AWS S3).

---

## Features

- Fetches live NBA player stats via API  
- Cleans and filters data with pandas  
- Normalizes key metrics using z-scores  
- Applies weighted scoring to compute an MVP_SCORE  
- Ranks players and outputs Top 10 MVP candidates  
- Visualizes results with a bar chart  
- Persists MVP rankings in SQLite  
- Exports results to CSV and optionally uploads to AWS S3  

---

## MVP Scoring Model

Each player is evaluated using standardized (z-score) versions of the following stats:

- Points Per Game (PPG)  
- True Shooting % (TS_PCT)  
- Team Win % (W_PCT)  
- Plus/Minus (PLUS_MINUS)  
- Assists Per Game (APG)  
- Rebounds Per Game (RPG)  

Weights:

- PPG: 35%  
- TS_PCT: 15%  
- W_PCT: 20%  
- PLUS_MINUS: 20%  
- APG: 5%  
- RPG: 5%  

Final score


---

## Tech Stack

- Python  
- pandas  
- SQLite (local persistence)  
- matplotlib (visualization)  
- AWS S3 (optional export)  

---

## How to Run

1. Clone the repo and create a virtual environment.  
2. Install dependencies:

```bash
pip install -r requirements.txt



"""Pull real-world F1 constructor (team) standings from the Jolpica-F1 API.

fetch_f1_results.py pulls driver standings only. Constructor standings are
needed separately to control for car/team quality: a driver's raw points
total is a joint function of driving skill and machinery, and this project's
first notebook doesn't disentangle the two. Having each constructor's
season points alongside driver points lets us compute car-adjusted metrics
(e.g. driver points as a share of constructor points, or vs teammate).

No API key is required. Docs: https://github.com/jolpica/jolpica-f1

Output: data/raw/f1_constructorstandings_{season}.csv
"""

import os
import time

import pandas as pd
import requests

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
BASE_URL = "https://api.jolpi.ca/ergast/f1"
SEASONS = [2025, 2026]
HEADERS = {"User-Agent": "Mozilla/5.0 (f1-driver-ratings-analysis research script)"}


def fetch_constructor_standings(season):
    url = f"{BASE_URL}/{season}/constructorstandings.json"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    tables = data["MRData"]["StandingsTable"]["StandingsLists"]
    if not tables:
        return pd.DataFrame(), None
    standings_list = tables[0]
    round_reached = standings_list.get("round")
    rows = []
    for entry in standings_list["ConstructorStandings"]:
        team = entry["Constructor"]
        rows.append({
            "season": season,
            "round_reached": round_reached,
            "position": int(entry["position"]),
            "points": float(entry["points"]),
            "wins": int(entry["wins"]),
            "constructor_id": team["constructorId"],
            "constructor": team["name"],
        })
    return pd.DataFrame(rows), round_reached


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    for season in SEASONS:
        df, round_reached = fetch_constructor_standings(season)
        if df.empty:
            print(f"season {season}: no data returned, skipping")
            continue
        out_path = os.path.join(RAW_DIR, f"f1_constructorstandings_{season}.csv")
        df.to_csv(out_path, index=False)
        print(f"season {season} (through round {round_reached}): "
              f"{len(df)} constructors -> {out_path}")
        time.sleep(1)  # be polite to the free API


if __name__ == "__main__":
    main()

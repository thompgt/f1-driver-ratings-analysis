"""Pull real-world F1 driver standings from the Jolpica-F1 API.

Jolpica-F1 (https://github.com/jolpica/jolpica-f1) is the actively-maintained,
community-run successor to the Ergast API, which shut down in 2024. It mirrors
Ergast's JSON schema and URL layout, just on a new host.

We pull full-season driver standings for:
  - 2025: a complete season, used as the more statistically stable
    ground-truth comparison.
  - 2026: the current (in-progress, as of this writing) season -- the one the
    "2026 Season Pack" ratings are actually meant to reflect, but note it's a
    partial season (whatever round has been reached at fetch time), so points
    totals aren't directly comparable to a full season and early-season
    variance is higher.

No API key is required. Docs: https://github.com/jolpica/jolpica-f1
"""

import os
import time

import pandas as pd
import requests

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
BASE_URL = "https://api.jolpi.ca/ergast/f1"
SEASONS = [2025, 2026]
HEADERS = {"User-Agent": "Mozilla/5.0 (f1-driver-ratings-analysis research script)"}


def fetch_standings(season):
    url = f"{BASE_URL}/{season}/driverstandings.json"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    tables = data["MRData"]["StandingsTable"]["StandingsLists"]
    if not tables:
        return pd.DataFrame(), None
    standings_list = tables[0]
    round_reached = standings_list.get("round")
    rows = []
    for entry in standings_list["DriverStandings"]:
        drv = entry["Driver"]
        constructors = entry.get("Constructors", [])
        rows.append({
            "season": season,
            "round_reached": round_reached,
            "position": int(entry["position"]),
            "points": float(entry["points"]),
            "wins": int(entry["wins"]),
            "driver_id": drv["driverId"],
            "given_name": drv["givenName"],
            "family_name": drv["familyName"],
            "nationality": drv.get("nationality"),
            "constructor": constructors[0]["name"] if constructors else None,
        })
    return pd.DataFrame(rows), round_reached


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    for season in SEASONS:
        df, round_reached = fetch_standings(season)
        if df.empty:
            print(f"season {season}: no data returned, skipping")
            continue
        out_path = os.path.join(RAW_DIR, f"f1_driverstandings_{season}.csv")
        df.to_csv(out_path, index=False)
        print(f"season {season} (through round {round_reached}): "
              f"{len(df)} drivers -> {out_path}")
        time.sleep(1)  # be polite to the free API


if __name__ == "__main__":
    main()

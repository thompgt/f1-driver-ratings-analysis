"""Pull per-round qualifying and race results (with grid position) from the
Jolpica-F1 API.

fetch_f1_results.py already pulls season-end driver *standings* (final
points/position), which is enough for notebook 01's overall rating vs season
points comparison. It does not, however, separate raw one-lap qualifying pace
from race-day results, and doesn't capture grid position -- both needed to
test whether the game's "Pace" attribute tracks qualifying performance better
than race performance, and whether "Racecraft" tracks positions gained during
races (finish position vs grid position) rather than just the scoreboard.

This script fetches, per round, for each season in SEASONS:
  - QualifyingResults (best grid-determining position reached in Q1/Q2/Q3)
  - Race Results (grid position, finish position, points, status)

The Jolpica-F1 API caps `limit` at 100 records per request regardless of what
is requested, so both endpoints are paginated with `offset` until the
API-reported `total` record count is reached.

No API key is required. Docs: https://github.com/jolpica/jolpica-f1

Outputs:
  data/raw/f1_qualifying_results.csv  (season, round, driver_id, given_name,
    family_name, constructor, quali_position)
  data/raw/f1_race_results.csv  (season, round, driver_id, given_name,
    family_name, constructor, grid, position, points, status)
"""

import os
import time

import pandas as pd
import requests

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
BASE_URL = "https://api.jolpi.ca/ergast/f1"
SEASONS = [2025, 2026]
PAGE_SIZE = 100
HEADERS = {"User-Agent": "Mozilla/5.0 (f1-driver-ratings-analysis research script)"}


def _paginated_races(url):
    """Yield all Race entries from a Jolpica RaceTable endpoint, paginating
    with offset/limit since the API silently caps limit at 100 records."""
    offset = 0
    while True:
        resp = requests.get(url, headers=HEADERS,
                             params={"limit": PAGE_SIZE, "offset": offset}, timeout=30)
        resp.raise_for_status()
        data = resp.json()["MRData"]
        races = data["RaceTable"]["Races"]
        for race in races:
            yield race
        total = int(data["total"])
        returned = int(data["limit"])
        offset += returned
        if offset >= total or not races:
            break
        time.sleep(0.3)  # be polite to the free API between pages


def fetch_qualifying(season):
    rows = []
    for race in _paginated_races(f"{BASE_URL}/{season}/qualifying.json"):
        round_no = int(race["round"])
        for entry in race.get("QualifyingResults", []):
            drv = entry["Driver"]
            rows.append({
                "season": season,
                "round": round_no,
                "driver_id": drv["driverId"],
                "given_name": drv["givenName"],
                "family_name": drv["familyName"],
                "constructor": entry["Constructor"]["name"],
                "quali_position": int(entry["position"]),
            })
    return pd.DataFrame(rows)


def fetch_race_results(season):
    rows = []
    for race in _paginated_races(f"{BASE_URL}/{season}/results.json"):
        round_no = int(race["round"])
        for entry in race.get("Results", []):
            drv = entry["Driver"]
            # grid == 0 means started from pit lane; treat as missing for
            # positions-gained purposes rather than a fake starting slot.
            grid = int(entry["grid"])
            rows.append({
                "season": season,
                "round": round_no,
                "driver_id": drv["driverId"],
                "given_name": drv["givenName"],
                "family_name": drv["familyName"],
                "constructor": entry["Constructor"]["name"],
                "grid": grid if grid > 0 else None,
                "position": int(entry["position"]) if entry["position"].isdigit() else None,
                "points": float(entry["points"]),
                "status": entry["status"],
            })
    return pd.DataFrame(rows)


def main():
    os.makedirs(RAW_DIR, exist_ok=True)

    quali_frames, race_frames = [], []
    for season in SEASONS:
        q = fetch_qualifying(season)
        quali_frames.append(q)
        print(f"season {season}: {len(q)} qualifying results "
              f"across {q['round'].nunique()} rounds")
        time.sleep(1)

        r = fetch_race_results(season)
        race_frames.append(r)
        print(f"season {season}: {len(r)} race results "
              f"across {r['round'].nunique()} rounds")
        time.sleep(1)

    quali_out = os.path.join(RAW_DIR, "f1_qualifying_results.csv")
    race_out = os.path.join(RAW_DIR, "f1_race_results.csv")
    pd.concat(quali_frames, ignore_index=True).to_csv(quali_out, index=False)
    pd.concat(race_frames, ignore_index=True).to_csv(race_out, index=False)
    print(f"wrote -> {quali_out}")
    print(f"wrote -> {race_out}")


if __name__ == "__main__":
    main()

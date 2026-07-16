"""Merge the hand-compiled F1 25 (2026 Season Pack) driver ratings with real
2025/2026 season results from Jolpica-F1, by normalized driver family name.

There are only ~20-22 drivers involved, so unlike the FIFA/FC project's
fuzzy-matching pipeline (rapidfuzz + age-blocking over ~18k players), a simple
normalized-last-name join is enough here -- small enough to eyeball by hand.

Output: data/processed/f1_ratings_vs_results.csv
"""

import os
import unicodedata

import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROC_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


def normalize_name(name):
    if pd.isna(name):
        return ""
    name = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode()
    return name.lower().strip()


def last_name(full_name):
    return normalize_name(full_name).split(" ")[-1]


def load_ratings():
    df = pd.read_csv(os.path.join(RAW_DIR, "f1_25_2026_season_pack_ratings.csv"))
    df["name_key"] = df["driver"].map(last_name)
    return df


def load_standings(season):
    path = os.path.join(RAW_DIR, f"f1_driverstandings_{season}.csv")
    df = pd.read_csv(path)
    df["name_key"] = df["family_name"].map(last_name)
    df = df.rename(columns={
        "position": f"position_{season}",
        "points": f"points_{season}",
        "wins": f"wins_{season}",
        "round_reached": f"round_reached_{season}",
        "constructor": f"constructor_{season}",
    })
    keep = ["name_key", f"position_{season}", f"points_{season}", f"wins_{season}",
            f"round_reached_{season}", f"constructor_{season}"]
    return df[keep]


def main():
    os.makedirs(PROC_DIR, exist_ok=True)

    ratings = load_ratings()
    s2025 = load_standings(2025)
    s2026 = load_standings(2026)

    merged = ratings.merge(s2025, on="name_key", how="left")
    merged = merged.merge(s2026, on="name_key", how="left")
    merged = merged.drop(columns=["name_key"])

    out_path = os.path.join(PROC_DIR, "f1_ratings_vs_results.csv")
    merged.to_csv(out_path, index=False)

    n_2025 = merged["points_2025"].notna().sum()
    n_2026 = merged["points_2026"].notna().sum()
    print(f"wrote {len(merged)} drivers -> {out_path}")
    print(f"matched to 2025 standings: {n_2025}/{len(merged)}")
    print(f"matched to 2026 standings: {n_2026}/{len(merged)}")
    unmatched_2026 = merged.loc[merged["points_2026"].isna(), "driver"].tolist()
    if unmatched_2026:
        print(f"no 2026 result for: {unmatched_2026} (rookie not yet on grid, "
              f"or Ergast/Jolpica driverId spelling mismatch)")


if __name__ == "__main__":
    main()

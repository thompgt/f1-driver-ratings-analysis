"""Compile the F1 25 (2026 Season Pack) in-game driver ratings into a CSV.

IMPORTANT / HONESTY NOTE: unlike the FIFA/FC project's `fetch_fc26.py`, this is
NOT a general-purpose scraper. There is no structured, downloadable dataset of
these ratings (no Kaggle dataset, no public API) -- EA's own ratings page
(https://www.ea.com/games/f1/ratings) renders the table client-side via
JavaScript, and the gaming-press writeups that cover it are ordinary prose
articles, not machine-readable tables. This script is a manual/semi-manual
compilation: the numbers below were transcribed by hand from press coverage
(see SOURCES) during the July 2026 research pass for this project, then
hardcoded here so the pipeline is at least reproducible and versioned.

Scope reality check: EA did not release a standalone annual "F1 26" game.
Instead they released a paid DLC, "F1 25: 2026 Season Pack" (launched June
2026), which updates car liveries, the 2026 grid/driver lineup, and driver
ratings for the new season. The next full numbered title is planned for 2027.
This project analyzes those F1 25 (2026 Season Pack) ratings -- not a
fictitious "F1 26" game.

Rating scale: each driver gets an Overall rating (0-100) built from four
sub-attributes also on a 0-100 scale:
  - EXP (Experience): built up over a driver's career, older/longer-tenured
    drivers tend to score higher here regardless of current form.
  - RAC (Racecraft): overtaking / wheel-to-wheel ability.
  - AWA (Awareness): clean driving, avoiding incidents/penalties.
  - PAC (Pace): raw one-lap/race speed vs. the rest of the grid.

SOURCES (all accessed July 2026):
  - EA Sports official ratings page & reveal posts (methodology, headline
    numbers, confirms Verstappen 95 / Norris 94 at launch):
      https://www.ea.com/games/f1/ratings
      https://www.ea.com/games/f1/f1-25/news/f1-25-2026-season-pack-driver-ratings
  - GiveMeSport, "The Driver Ratings For F1 26 Have Been Released" (top-10
    headline numbers, rating methodology description):
      https://www.givemesport.com/f1-driver-ratings-2026-season/
  - ClutchPoints / Yahoo Sports syndication, "F1 25 2026 Season Pack All
    Driver Ratings at Launch" (the only source found with a complete 22-driver
    table INCLUDING the four sub-attributes -- this is the primary source for
    the per-attribute breakdown used below):
      https://clutchpoints.com/gaming/f1-25-2026-season-pack-all-driver-ratings
      https://sports.yahoo.com/articles/f1-25-2026-season-pack-190717327.html
  - SportsKeeda, "All new driver ratings in F1 25 2026 Season" (cross-check
    on headline Overall numbers):
      https://www.sportskeeda.com/esports/all-new-driver-ratings-f1-25-2026-season

CAVEATS:
  - This is the LAUNCH (June 2026) table. EA pushes periodic in-season rating
    updates -- e.g. an official "June Update" piece
    (https://www.ea.com/games/f1/f1-25/news/f1-25-2026-season-pack-june-driver-ratings-update)
    already lists further tweaks (Norris 94->92, Antonelli +5 to 88, etc.)
    reflecting early/mid 2026 season form. We freeze on the launch snapshot
    here for a single stable, fully-attributed table; treat these numbers as
    approximate/best-effort press compilations, not an authoritative EA export.
  - Team names are simplified/current as of the 2026 grid (e.g. "Audi" for
    the rebranded Sauber-based team, "Racing Bulls" for the Red Bull junior
    team, "Cadillac" for the new entrant).
"""

import os

import pandas as pd

PROC_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# rank, driver, team, overall, experience, racecraft, awareness, pace
RATINGS = [
    (1, "Max Verstappen", "Red Bull Racing", 95, 87, 96, 85, 96),
    (2, "Lando Norris", "McLaren", 94, 81, 89, 80, 94),
    (3, "George Russell", "Mercedes", 93, 83, 94, 93, 94),
    (4, "Charles Leclerc", "Ferrari", 92, 83, 92, 91, 93),
    (5, "Lewis Hamilton", "Ferrari", 91, 98, 93, 91, 89),
    (6, "Oscar Piastri", "McLaren", 91, 77, 95, 81, 92),
    (7, "Fernando Alonso", "Aston Martin", 90, 99, 90, 81, 87),
    (8, "Carlos Sainz", "Williams", 86, 88, 88, 80, 86),
    (9, "Alexander Albon", "Williams", 85, 84, 87, 77, 85),
    (10, "Sergio Perez", "Cadillac", 85, 92, 83, 81, 85),
    (11, "Nico Hulkenberg", "Audi", 85, 88, 85, 85, 85),
    (12, "Pierre Gasly", "Alpine", 84, 83, 83, 78, 85),
    (13, "Valtteri Bottas", "Cadillac", 84, 89, 75, 95, 87),
    (14, "Esteban Ocon", "Haas", 84, 83, 85, 84, 84),
    (15, "Kimi Antonelli", "Mercedes", 83, 70, 83, 75, 85),
    (16, "Isack Hadjar", "Racing Bulls", 83, 71, 81, 82, 85),
    (17, "Oliver Bearman", "Haas", 83, 72, 88, 70, 83),
    (18, "Gabriel Bortoleto", "Audi", 80, 69, 81, 77, 81),
    (19, "Liam Lawson", "Racing Bulls", 79, 73, 79, 71, 81),
    (20, "Lance Stroll", "Aston Martin", 77, 84, 77, 73, 77),
    (21, "Franco Colapinto", "Alpine", 73, 69, 71, 74, 75),
    (22, "Arvid Lindblad", "Racing Bulls", 68, 32, 70, 60, 72),
]

COLUMNS = [
    "launch_rank", "driver", "team", "overall",
    "experience", "racecraft", "awareness", "pace",
]


def main():
    os.makedirs(PROC_DIR, exist_ok=True)
    df = pd.DataFrame(RATINGS, columns=COLUMNS)
    out_path = os.path.join(PROC_DIR, "f1_25_2026_season_pack_ratings.csv")
    df.to_csv(out_path, index=False)
    print(f"wrote {len(df)} drivers -> {out_path}")


if __name__ == "__main__":
    main()

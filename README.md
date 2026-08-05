# F1 25 (2026 Season Pack) Driver Ratings vs. Real-World Performance

A small data-science project comparing EA Sports' in-game F1 driver ratings
against actual 2025/2026 Formula 1 season results, loosely modeled on the
[`fifa-analysis`](../fifa-analysis) project's structure (data acquisition
scripts -> merged CSV -> notebook), but scaled down to fit a much thinner data
situation: ~20 drivers instead of ~18k players, and no structured source for
the ratings at all.

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

## Scope reality check (read this first)

There is **no standalone "F1 26" video game**. EA/Codemasters did not release
an annual F1 26 title. Instead, in June 2026 they released a paid DLC for the
existing game: **"F1 25: 2026 Season Pack"**, which updates the grid/liveries
for the 2026 season and refreshes driver ratings accordingly. The next full
numbered game is planned for 2027. Gaming press coverage is inconsistent about
this and several outlets casually call it "F1 26 driver ratings" in headlines
-- this project uses the accurate name throughout and analyzes the F1 25:
2026 Season Pack ratings, not a fictitious game.

Also, unlike football (FIFA/FC) or basketball, **Formula 1 has no per-driver
"market value" concept** -- there's no transfer-fee market for drivers in the
same sense. So the `fifa-analysis` project's notebook 04 "moneyball" /
value-prediction section has **no analog here** and is intentionally omitted
rather than forced onto data that doesn't support it.

## Data sources

- **In-game ratings**: there is no downloadable dataset or API for these --
  EA's own [ratings page](https://www.ea.com/games/f1/ratings) renders its
  table client-side via JavaScript, and there's no Kaggle dataset. The ~22-row
  table used here (`scripts/compile_driver_ratings.py`) was **hand-compiled**
  from gaming-press coverage of the June 2026 launch of the 2026 Season Pack:
  - [EA Sports official ratings page](https://www.ea.com/games/f1/ratings) and
    [reveal post](https://www.ea.com/games/f1/f1-25/news/f1-25-2026-season-pack-driver-ratings)
    -- methodology and headline numbers.
  - [GiveMeSport, "The Driver Ratings For F1 26 Have Been Released"](https://www.givemesport.com/f1-driver-ratings-2026-season/)
    -- top-10 headline numbers and methodology description.
  - [ClutchPoints / Yahoo Sports syndication, "F1 25 2026 Season Pack All Driver Ratings at Launch"](https://sports.yahoo.com/articles/f1-25-2026-season-pack-190717327.html)
    -- the only source found with the **complete 22-driver table including
    the four sub-attributes** (Experience, Racecraft, Awareness, Pace); this
    is the primary source for the per-attribute numbers used below.
  - [SportsKeeda, "All new driver ratings in F1 25 2026 Season"](https://www.sportskeeda.com/esports/all-new-driver-ratings-f1-25-2026-season)
    -- cross-check on headline Overall numbers.

  **Treat these numbers as approximate/best-effort press compilations**, not
  an authoritative EA export. They also reflect a single snapshot -- the June
  2026 launch table -- while EA pushes periodic in-season updates (a
  [June update post](https://www.ea.com/games/f1/f1-25/news/f1-25-2026-season-pack-june-driver-ratings-update)
  already lists further tweaks, e.g. Norris 94->92 as his form dipped, and
  Antonelli +5 to 88 as he took the championship lead). Freezing on the launch
  snapshot keeps the sub-attribute table complete and internally consistent.

- **Real-world results**: full driver standings for the **2025** season
  (complete) and the **2026** season (in progress, partial) via
  [Jolpica-F1](https://github.com/jolpica/jolpica-f1), the actively-maintained,
  community-run successor to the Ergast API (which shut down in 2024). No API
  key needed; `scripts/fetch_f1_results.py` hits
  `https://api.jolpi.ca/ergast/f1/{season}/driverstandings.json`.

## Project structure

```
scripts/
  compile_driver_ratings.py   hand-compiled ratings table -> CSV (see notes in file header)
  fetch_f1_results.py         pulls 2025 + 2026 driver standings from Jolpica-F1
  build_dataset.py            merges ratings + standings by normalized driver name
data/
  raw/                        untracked, gitignored (regenerate via scripts/)
  processed/                  merged CSV, tracked in git
notebooks/
  01_ratings_vs_performance.ipynb   ratings vs. real-world results: correlation,
                                    scatter plot, over/under-rated ranking
```

## Reproducing

```
pip install -r requirements.txt
python scripts/compile_driver_ratings.py
python scripts/fetch_f1_results.py
python scripts/build_dataset.py
jupyter notebook
```

No API keys or credentials are required for any step.

## Honest limitations

- **N ~= 20-22 drivers.** This supports descriptive correlations and a ranked
  over/under-rated table, and nothing more -- no train/test splits, no
  significance testing that would mean much, no clustering, no value
  modeling. Every claim in the notebook is framed as descriptive, not
  statistically powered.
- The ratings table is a **manual compilation from press coverage**, not a
  scrape of a structured source -- treat individual numbers as approximate.
- The 2026 season standings are a **partial season snapshot** (as of whatever
  round Jolpica-F1 had recorded at fetch time), so points totals for 2025 vs.
  2026 aren't on the same scale; the notebook treats them as separate
  comparisons rather than pooling them.

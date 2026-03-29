# Football Player Comparison Tool
 
A desktop application for comparing football (soccer) players across Europe's top five leagues. Select any two positionally compatible players and generate a side-by-side radar chart of their key performance metrics, normalised per 90 minutes.
 
---
 
## Features
 
- **Player browser** — searchable, filterable table of players across the Premier League, La Liga, Bundesliga, Serie A, and Ligue 1
- **Dual-panel selection** — pick one player per panel; filters include name, league, country, and position
- **Compatibility check** — the "Generate graph" button is only enabled when both players share a compatible position group (e.g. two central midfielders, two wingers)
- **Radar chart** — interactive Plotly chart rendered in-app, with per-90 normalised stats and hover tooltips showing raw values
- **Data pipeline** — automated scraper that fetches player stats from the SofaScore API and enriches positions via the SportDB API
 
---
 
## Demo
 
<video src="https://raw.githubusercontent.com/markusm1901/Football-Player-Comparison-Tool/main/images/demo.mp4" controls width="100%"></video>
 
---

## Project Structure

```
├── main.py                        # Entry point
├── src/
│   ├── config.py                  # League IDs, position mappings, metric groups
│   ├── data_scraper.py            # Async SofaScore scraper
│   └── data_cleaner.py            # CSV utilities, name/team fixes, position enrichment
├── components/
│   ├── main_window.py             # QMainWindow, view switching
│   ├── select_player_view.py      # Dual-panel selection layout
│   ├── player_view.py             # Filterable player table widget
│   └── chart_view.py             # Plotly radar chart widget
└── data/
    └── players_data.csv           # Cached player data (auto-generated on first run)
```

---

## How It Works

### 1. Data pipeline

On first launch, if `players_data.csv` is not found, the app runs a three-step pipeline:

1. **Scrape** — `data_scraper.py` fetches the current season's player statistics from the SofaScore API for all five configured leagues using async HTTP requests (via `curl_cffi`). Only players with more than 720 minutes played are kept. 
2. **Clean** — `data_cleaner.repair()` applies known name and team fixes to align SofaScore spellings with the position-enrichment API.
3. **Enrich** — `data_cleaner.change_positions()` calls the SportDB / Transfermarkt API to replace generic positions (e.g. `Midfielder`) with granular ones (e.g. `CM`, `DM`, `AM`). Results are saved back to CSV.

I am uploading an already ready to work on file due to the time it takes to scrape all of this data (whole process takes about 15-20min).It is that long because I needed to avoid getting 403 HTTP error and also SportsDB free plan only allows to make 3 calls per second. Should you wish to update the file, you will need to create 2 accounts and 2 new API keys on SportsDB, and replace them in config.py file (1 free API key allows only up to 1000 calls and there's a little more then 1400 players). In the future there's an option of storing the data in a database which will be automatically updated after each matchweek.

### 2. Player selection

The selection screen shows two `PlayersView` panels side by side. Each panel loads the full player dataset and offers four filters:

| Filter | Type |
|---|---|
| Name | Free-text search (case-insensitive) |
| League | Dropdown |
| Country | Dropdown |
| Position | Dropdown |

When a player is selected in each panel, their positions are checked against `COMPATIBLE_GROUPS` in `config.py`. The "Generate graph" button is enabled only if both positions belong to the same group.

### 3. Radar chart

The chart screen renders a Plotly `Scatterpolar` (radar) chart inside a `QWebEngineView`. Metrics are:

- Filtered to the relevant position group (from `config.py`)
- Normalised per 90 minutes (except percentage-based stats)
- Scaled to 0–100 relative to the higher of the two players for each metric
- Displayed with hover tooltips showing the actual per-90 value

---

## Position Groups & Metrics

Metrics plotted depend on the shared position group of the two selected players:

| Group | Positions |
|---|---|
| Central midfielders | CM, DM |
| Attacking midfielders | AM, SS |
| Centre backs | CB |
| Full backs / wide midfielders | LB, RB, LM, RM |
| Strikers | CF, SS |
| Goalkeepers | GK |
| Wingers | LW, RW |

---

## Requirements

- Python 3.9+
- PySide2
- pandas
- plotly
- curl_cffi
- requests
- qt-material

Install all dependencies:

```bash
pip install PySide2 pandas plotly curl_cffi requests qt-material
```

---

## Running the App

```bash
python main.py
```
---
## Configuration

All configuration lives in `src/config.py`:

| Constant | Description |
|---|---|
| `PLAYERS_DATA_PATH` | Path to the cached CSV file |
| `LEAGUES` | League names mapped to SofaScore tournament IDs |
| `POSITION_MAP` | Maps single-letter positions (`G`, `D`, `M`, `F`) to display names |
| `COMPATIBLE_GROUPS` | Maps position tuples to their metric lists |
| `DISPLAY_LEAGUES` | Ordered list of league names shown in the filter dropdown |
| `HEADERS` | HTTP headers used for SofaScore API requests |

---

## Known Limitations
- Position enrichment (`change_positions`) runs synchronously and blocks startup; it is best run as a one-off offline script rather than on every first launch.
- The SofaScore API is unofficial and undocumented; breaking changes may occur without notice.

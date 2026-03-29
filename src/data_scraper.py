from . import config
# from understat import Understat
import asyncio
import pandas as pd
from datetime import datetime
from curl_cffi import requests as cffi_requests
from curl_cffi.requests import AsyncSession
def get_season_and_players(tournament_id):
    season_url = f"https://api.sofascore.com/api/v1/unique-tournament/{tournament_id}/seasons"
    res = cffi_requests.get(season_url, headers=config.HEADERS, impersonate="chrome110")
    if res.status_code != 200:
        return []
        
    season_id = res.json()['seasons'][0]['id']
    players = []
    offset = 0
    
    while True:
        url = f"https://api.sofascore.com/api/v1/unique-tournament/{tournament_id}/season/{season_id}/statistics?limit=100&order=-rating&offset={offset}&accumulation=total"
        r = cffi_requests.get(url, headers=config.HEADERS, impersonate="chrome110")
        if r.status_code != 200 or not r.json().get('results'):
            break
        for row in r.json()['results']:
            if 'player' in row:
                players.append({
                    'player_id': row['player']['id'],
                    'player_name': row['player']['name'],
                    'season_id': season_id
                })
        offset += 100
    return players

async def fetch_player_details(session, player, tournament_id, league_name, semaphore):
    async with semaphore: 
        profile_url = f"https://api.sofascore.com/api/v1/player/{player['player_id']}"
        stats_url = f"https://api.sofascore.com/api/v1/player/{player['player_id']}/unique-tournament/{tournament_id}/season/{player['season_id']}/statistics/overall"
        profile_res = await session.get(profile_url, headers=config.HEADERS)
        if profile_res.status_code != 200:
            return None
        profile_data = profile_res.json().get('player', {})
        country = profile_data.get('country', {}).get('name', 'Unknown')
        raw_pos = profile_data.get('position', '')
        position = config.POSITION_MAP.get(raw_pos, raw_pos) 
        age = None
        dob_timestamp = profile_data.get('dateOfBirthTimestamp')
        if dob_timestamp:
            birth_date = datetime.fromtimestamp(dob_timestamp)
            now = datetime.now()
            age = now.year - birth_date.year - ((now.month, now.day) < (birth_date.month, birth_date.day))
        stats_res = await session.get(stats_url, headers=config.HEADERS)
        if stats_res.status_code == 200:
            data = stats_res.json()
            stats = data.get("statistics", {})
            stats["team"] = data.get("team", {}).get("name", "")
            stats['player_id'] = player['player_id']
            stats['player_name'] = player['player_name']
            stats['league'] = league_name
            stats['age'] = age
            stats['position'] = position
            stats['country'] = country
            if 'statisticsType' in stats:
                del stats['statisticsType']
            return stats
        else:
            return None

async def download_all_leagues_fast():
    semaphore = asyncio.Semaphore(5) 
    all_results = []
    async with AsyncSession(impersonate="chrome110") as session:
        for league_name, tournament_id in config.LEAGUES.items():
            players = get_season_and_players(tournament_id)
            chunk_size = 20
            for i in range(0, len(players), chunk_size):
                chunk = players[i : i + chunk_size]
                tasks = [
                    fetch_player_details(session, p, tournament_id, league_name, semaphore) 
                    for p in chunk
                ]
                chunk_results = await asyncio.gather(*tasks)
                valid_stats = [s for s in chunk_results if s]
                all_results.extend(valid_stats)
                await asyncio.sleep(2)
    return all_results
def save_to_csv(results):
    df = pd.DataFrame(results)
    front_cols = ['player_name', 'team', 'league', 'age', 'position', 'country']
    existing_front_cols = [c for c in front_cols if c in df.columns]
    other_cols = [c for c in df.columns if c not in existing_front_cols]
    df = df[existing_front_cols + other_cols]
    df = df[df["minutesPlayed"] > 720]
    df.to_csv(config.PLAYERS_DATA_PATH, index=False)
    
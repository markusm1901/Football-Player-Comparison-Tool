from PySide2.QtGui import QStandardItem
from src import config
import pandas as pd
import requests
import urllib.parse
import time
def get_player_position(player_name, api_key):
    encoded_name = urllib.parse.quote(player_name)
    url = "https://api.sportdb.dev/api/transfermarkt/players/search/" + encoded_name
    headers = {
        "X-API-Key": api_key,
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["results"]
def repair(df):
    name_fixes = {
        "Đorđe Petrović": "Djordje Petrovic",
        "Eli Junior Kroupi": "Junior Kroupi",
        "Josep Chavarría": "Pep Chavarria",
        "Abdelkabir Abqar": "Abdel Abqar",
        "Abdel Rahim": "Rahim Alhassane",
        "Marc-Oliver Kempf": "Marc Oliver Kempf",
        "Mutassim Al-Musrati": "Moatasem Al-Musrati",
        "Bernardo Silva": "Bernardo",
        "Haktab Omar Traore": "Omar Traore",
        "Pierre Lees Melou": "Pierre Lees-Melou",
        "Igor Silva": "Igor Sil",
        "André Silva": "André Sil",
        "Cheick Tidiane Sabaly": "Cheikh Sabaly"
    }
    team_fixes = {
        "Atlético Madrid": "Atlético de Madrid",
        "FC Bayern München": "Bayern Munich",
        "1. FC Union Berlin": "1.FC Union Berlin",
        "1. FSV Mainz 05": "1.FSV Mainz 05",
        "1. FC Heidenheim": "1.FC Heidenheim 1846",
        "TSG Hoffenheim": "TSG 1899 Hoffenheim",
        "1. FC Köln": "1.FC Köln",
        "Borussia M'gladbach": "Borussia Mönchengladbach",
        "Olympique de Marseille": "Olympique Marseille",
        "Olympique Lyonnais": "Olympique Lyon",
        "Athletic Club": "Athletic Bilbao",
        "Celta Vigo": "Celta de Vigo"
    }
    df["player_name"] = df["player_name"].replace(name_fixes)
    df["team"] = df["team"].replace(team_fixes)
    return df
def change_positions(df):
    for i in range(0, len(df)):
        current_api_key = config.API_KEY[0] if i < 1000 else config.API_KEY[1]
        result = get_player_position(df.loc[i, 'player_name'],current_api_key)
        if len(result)>0:
            club = df.loc[i, 'team']
            for player in result:
                if club in str(player["club"]["name"]):
                    df.loc[i, 'position'] = player["position"]   
                    break  
        else:
            df.loc[i, 'position'] = result["position"]
        time.sleep(0.34)
    df.to_csv(config.PLAYERS_DATA_PATH, index = False)
     
def get_data_csv(path: str):
    df = pd.read_csv(path)
    return df

def fill_Qtableview(df, cols, leagues, model):
            model.setRowCount(0)
            for row in range(len(df)):
                for col in range(len(cols)):
                    displayed_tmp = df.iat[row, col]
                    item_text = str(displayed_tmp)
                    item = QStandardItem(item_text)
                    item.setEditable(False) 
                    model.setItem(row, col, item)
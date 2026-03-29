DISPLAY_LEAGUES = ['All','Premier League','La Liga','Bundesliga','Ligue 1','Serie A']
PLAYERS_DATA_PATH = "./data/players_data.csv"
LEAGUES = {
    'Premier League': 17,
    'La Liga': 8,
    'Serie A': 23,
    'Bundesliga': 35,
    'Ligue 1': 34
}

HEADERS = {
    "Origin": "https://www.sofascore.com",
    "Referer": "https://www.sofascore.com/"
}

POSITION_MAP = {
    'G': 'Goalkeeper',
    'D': 'Defender',
    'M': 'Midfielder',
    'F': 'Forward'
}
COMPATIBLE_GROUPS = {
    ("CM", "DM"): ["touches", "keyPasses", "accurateOppositionHalfPasses", "interceptions", "groundDuelsWon","ballRecovery","accuratePassesPercentage", "passToAssist","minutesPlayed"],
    ("AM", "SS"): ["successfulDribbles","goalsAssistsSum", "bigChancesCreated","possessionWonAttThird", "bigChancesMissed","ballRecovery","keyPasses","expectedAssists","minutesPlayed"],
    ("CB",): ["minutesPlayed","accuratePassesPercentage","interceptions", "tacklesWonPercentage","groundDuelsWonPercentage","aerialDuelsWonPercentage", "accurateLongBallsPercentage","clearances","errorLeadToGoal","dribbledPast"],
    ("LB", "RB", "LM", "RM"): ["accurateCrossesPercentage","interceptions", "tacklesWonPercentage", "successfulDribbles","keyPasses","accurateFinalThirdPasses","groundDuelsWonPercentage","dribbledPast","minutesPlayed"],
    ("CF", "SS"): ["minutesPlayed", "goals", "bigChancesMissed", "aerialDuelsWonPercentage", "shotsOnTarget", "expectedGoals", "possessionWonAttThird","wasFouled"],
    ("GK",): ["minutesPlayed", "saves", "cleanSheet", "punches","runsOut","highClaims","penaltyFaced", "penaltySave","accurateLongBallsPercentage"],
    ("LW", "RW"): ["successfulDribbles","goalsAssistsSum", "bigChancesCreated","possessionWonAttThird", "bigChancesMissed","ballRecovery","keyPasses","expectedAssists","minutesPlayed","possessionLost"]
}
API_KEY = ["Rd01VWmNyjVamSalzukjdiGRuu1fAMj7P2jdXf7y","aYvCMDSVfgMcAjrErtv3v8VSMVHu8rdodTFiextj"]
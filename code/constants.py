TEAM_NAME_MAP = {
    "atlanta hawks": "atlanta hawks",
    "boston celtics": "boston celtics",
    "brooklyn nets": "brooklyn nets",
    "new jersey nets": "brooklyn nets", 
    "charlotte hornets": "charlotte hornets",
    "charlotte bobcats": "charlotte hornets", 
    "chicago bulls": "chicago bulls",
    "cleveland cavaliers": "cleveland cavaliers",
    "dallas mavericks": "dallas mavericks",
    "denver nuggets": "denver nuggets",
    "detroit pistons": "detroit pistons",
    "golden state warriors": "golden state warriors",
    "houston rockets": "houston rockets",
    "indiana pacers": "indiana pacers",
    "los angeles clippers": "los angeles clippers",
    "san diego clippers": "los angeles clippers", 
    "los angeles lakers": "los angeles lakers",
    "memphis grizzlies": "memphis grizzlies",
    "vancouver grizzlies": "memphis grizzlies",
    "miami heat": "miami heat",
    "milwaukee bucks": "milwaukee bucks",
    "minnesota timberwolves": "minnesota timberwolves",
    "new orleans pelicans": "new orleans pelicans",
    "new orleans hornets": "new orleans pelicans", 
    "new orleansoklahoma city hornets": "new orleans pelicans", 
    "new york knicks": "new york knicks",
    "oklahoma city thunder": "oklahoma city thunder",
    "seattle supersonics": "oklahoma city thunder",
    "orlando magic": "orlando magic",
    "philadelphia 76ers": "philadelphia 76ers",
    "philadelphia ers": "philadelphia 76ers", 
    "philadelphia sixers": "philadelphia 76ers", 
    "phoenix suns": "phoenix suns",
    "portland trail blazers": "portland trail blazers",
    "sacramento kings": "sacramento kings",
    "kansas city kings": "sacramento kings", 
    "san antonio spurs": "san antonio spurs",
    "toronto raptors": "toronto raptors",
    "utah jazz": "utah jazz",
    "washington wizards": "washington wizards",
    "washington bullets": "washington wizards",
}

# draft coins
FIRST_PICK_COINS_COEF = 0
SECOND_PICK_COINS_COEF = 0.25
THIRD_PICK_COINS_COEF = 0.5
FOURTH_PICK_COINS_COEF = 0.75

# regular season coins
NO_PLAYOFFS_BONUS = 100
ROUND_1_LOSS_COEF = 1
ROUND_2_LOSS_COEF = 0.75
ROUND_3_LOSS_COEF = 0.5
FINAL_LOSS_COEF = 0.25
CHAMPION_COEF = 0


#===  SIMULATION  ===#

MIN_TEAM_STRENGTH = 60
MAX_TEAM_STRENGTH = 90
MAX_POSSIBLE_TEAM_STRENGTH = 100

GAMES_PER_TEAM_REGULAR_SEASON = 82 / (30-1)
MIN_NUMBER_OF_GAMES_BETWEEN_TWO_TEAMS = 2

# draft picks strength
DRAFT_PICK_STRENGTH = {
    1: 0.1317,
    2: 0.0983,
    3: 0.1052,
    4: 0.0973,
    5: 0.0921,
    6: 0.0784,
    7: 0.0859,
    8: 0.0664,
    9: 0.0954,
    10: 0.0899,
    11: 0.0862,
    12: 0.0670,
    13: 0.0799,
    14: 0.0655,
}

MIN_TEAM_STRENGTH_DECREASE = 0.02
MAX_TEAM_STRENGTH_DECREASE = 0.038



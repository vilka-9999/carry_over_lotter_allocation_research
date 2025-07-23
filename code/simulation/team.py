class Team:
    def __init__(self, name='some_team', total_wins=0, total_loses=0, total_games=0, season_wins=0, season_loses=0, season_games=0, season_rank=0, playoff_rank=0, coins=0, strength=0):
        self.name = name
        self.total_wins = total_wins        # Total number of wins across all seasons
        self.total_loses = total_loses      # Total number of losses across all seasons
        self.total_games = total_loses      # Total games
        self.season_wins = season_wins       # Wins in the current season
        self.season_loses = season_loses      # Losses in the current season
        self.season_games = season_games      # number of season games
        self.season_rank = season_rank       # Current season rank 
        self.playoff_rank = playoff_rank      # Playoff rank 
        self.coins = coins             # Number of coins
        self.strength = strength          # Strength of the team

    



class Team:
    def __init__(self, name='some_team', total_wins=0, total_loses=0, total_games=0, season_wins=0, season_loses=0, season_games=0, season_rank=0, playoff_rank=-1, coins=0, strength=0, season_draft_pick = 0):
        self.name = name
        self.total_wins = total_wins        # Total number of wins across all seasons
        self.total_loses = total_loses      # Total number of losses across all seasons
        self.total_games = total_loses      # Total games
        self.season_wins = season_wins       # Wins in the current season
        self.season_loses = season_loses      # Losses in the current season
        self.season_games = season_games      # number of season games
        self.season_rank = season_rank       # Current season rank 
        self.playoff_rank = playoff_rank      # Playoff rank 
        self.coins = coins                      # Number of coins
        self.strength = strength                # Strength of the team
        self.season_draft_pick = season_draft_pick  # draft pick   


    # clear the season stats
    def clear_season_stats(self):
        self.playoff_rank = -1
        self.season_wins = 0
        self.season_loses = 0
        self.season_games = 0
        self.season_rank = 0
        self.season_draft_pick = 0


    def __str__(self):
        return (
            f"Team: {self.name}\n"
            f"  Strength: {self.strength}\n"
            f"  Coins: {self.coins}\n"
            f"  Season: {self.season_wins}-{self.season_loses} (Games: {self.season_games}, Rank: {self.season_rank})\n"
            f"  Playoff Rank: {self.playoff_rank}\n"
            f"  Total: {self.total_wins}-{self.total_loses} (Games: {self.total_games})\n"
        )
    

    def __repr__(self):
        return self.__str__()
    



import random
from code.constants import DRAFT_PICK_STRENGTH, MIN_TEAM_STRENGTH_DECREASE, MAX_TEAM_STRENGTH_DECREASE, MAX_POSSIBLE_TEAM_STRENGTH


class Team:
    def __init__(self, name='some_team', total_wins=0, total_loses=0, total_games=0, season_wins=0, season_loses=0, season_games=0, season_rank=0, playoff_rank=-1, coins=0.0, strength=0, season_draft_pick = 0):
        self.name = name
        self.total_wins = total_wins        # Total number of wins across all seasons
        self.total_loses = total_loses      # Total number of losses across all seasons
        self.total_games = total_games      # Total games
        self.season_wins = season_wins       # Wins in the current season
        self.season_loses = season_loses      # Losses in the current season
        self.season_games = season_games      # number of season games
        self.season_rank = season_rank       # Current season rank 
        self.playoff_rank = playoff_rank      # Playoff rank 
        self.coins = coins                      # Number of coins
        self.strength = strength                # Strength of the team
        self.season_draft_pick = season_draft_pick  # draft pick   

        self.total_seasons_played = 0
        self.avg_season_wins = 0
        self.avg_coins = 0
        self.avg_strength = 0
        self.avg_season_rank = 0
        self.avg_playoff_rank = 0
        self.avg_draft_pick = 0


    # clear the season stats
    def clear_season_stats(self):
        self.playoff_rank = -1
        self.season_wins = 0
        self.season_loses = 0
        self.season_games = 0
        self.season_rank = 0


    def update_averages(self):
        if self.total_seasons_played > 0:
            self.avg_season_wins = (self.avg_season_wins * (self.total_seasons_played - 1) + self.season_wins)  / self.total_seasons_played
            self.avg_coins = (self.avg_coins * (self.total_seasons_played - 1) + self.coins)  / self.total_seasons_played
            self.avg_strength = (self.avg_strength * (self.total_seasons_played - 1) + self.strength)  / self.total_seasons_played
            self.avg_season_rank = (self.avg_season_rank * (self.total_seasons_played - 1) + self.season_rank) / self.total_seasons_played
            self.avg_playoff_rank = (self.avg_playoff_rank * (self.total_seasons_played - 1) + self.playoff_rank) / self.total_seasons_played
            self.avg_draft_pick = (self.avg_draft_pick * (self.total_seasons_played - 1) + self.season_draft_pick) / self.total_seasons_played


    def update_strength(self):

        # Decrease team strength after the season (players got old, etc.)
        decay = random.uniform(MIN_TEAM_STRENGTH_DECREASE, MAX_TEAM_STRENGTH_DECREASE)  # 7–12% loss
        self.strength *= (1 - decay)

        # 2. Draft pick boost (absolute gain from draft)
        coef = DRAFT_PICK_STRENGTH.get(self.season_draft_pick, 
                                       random.uniform(DRAFT_PICK_STRENGTH.get(13), DRAFT_PICK_STRENGTH.get(14)))
        draft_boost = coef * (MAX_POSSIBLE_TEAM_STRENGTH - self.strength)
        self.strength += draft_boost

        self.strength = min(MAX_POSSIBLE_TEAM_STRENGTH, round(self.strength, 2))




    def end_season(self):
        # Add season results to totals
        self.total_wins += self.season_wins
        self.total_loses += self.season_loses
        self.total_games += self.season_games
        self.total_seasons_played += 1

        # Update averages
        self.update_averages()


        


    def __str__(self):
        return (
            f"Team: {self.name}\n"
            f"  Strength: {self.strength:.2f}\n"
            f"  Coins: {self.coins:.2f}\n"
            f"  Season: {self.season_wins}-{self.season_loses} "
            f"(Games: {self.season_games}, Rank: {self.season_rank})\n"
            f"  Playoff Rank: {self.playoff_rank}\n"
            f"  Total: {self.total_wins}-{self.total_loses} "
            f"(Games: {self.total_games}, Seasons: {self.total_seasons_played})\n"
            f"  Draft Pick: {self.season_draft_pick}\n"
            f"  --- Averages ---\n"
            f"  Avg Season Wins: {self.avg_season_wins:.2f}\n"
            f"  Avg Coins: {self.avg_coins:.2f}\n"
            f"  Avg Strength: {self.avg_strength:.2f}\n"
            f"  Avg Season Rank: {self.avg_season_rank:.2f}\n"
            f"  Avg Playoff Rank: {self.avg_playoff_rank:.2f}\n"
            f"  Avg Draft Pick: {self.avg_draft_pick:.2f}\n" 
        )
    

    def __repr__(self):
        return self.__str__()
    

    def to_dict(self):
        return {
            "name": self.name,
            "total_wins": self.total_wins,
            "total_loses": self.total_loses,
            "total_games": self.total_games,
            "season_wins": self.season_wins,
            "season_loses": self.season_loses,
            "season_games": self.season_games,
            "season_rank": self.season_rank,
            "playoff_rank": self.playoff_rank,
            "coins": self.coins,
            "strength": self.strength,
            "season_draft_pick": self.season_draft_pick,
            "total_seasons_played": self.total_seasons_played,
            "avg_season_wins": self.avg_season_wins,
            "avg_coins": self.avg_coins,
            "avg_strength": self.avg_strength,
            "avg_season_rank": self.avg_season_rank,
            "avg_playoff_rank": self.avg_playoff_rank,
            "avg_draft_pick": self.avg_draft_pick,
        }
    



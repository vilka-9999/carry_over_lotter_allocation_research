import random
from code.constants import DRAFT_BOOST_COEF, DRAFT_PICK_STRENGTH, MIN_TEAM_STRENGTH_DECREASE, MAX_TEAM_STRENGTH_DECREASE, MAX_POSSIBLE_TEAM_STRENGTH


class Team:
    def __init__(self, name='some_team', total_wins=0, total_loses=0, total_games=0, season_wins=0, season_loses=0, season_games=0, season_rank=0, playoff_rank=-1, tickets=0.0, strength=0, season_draft_pick = 0):
        self.name = name
        self.total_wins = total_wins        # Total number of wins across all seasons
        self.total_loses = total_loses      # Total number of losses across all seasons
        self.total_games = total_games      # Total games
        self.season_wins = season_wins       # Wins in the current season
        self.season_loses = season_loses      # Losses in the current season
        self.season_games = season_games      # number of season games
        self.season_rank = season_rank       # Current season rank 
        self.playoff_rank = playoff_rank      # Playoff rank 
        self.tickets = tickets                      # Number of tickets
        self.strength = strength                # Strength of the team
        self.season_draft_pick = season_draft_pick  # draft pick   

        self.total_seasons_played = 0
        self.avg_season_wins = 0
        self.avg_tickets = 0
        self.avg_strength = 0
        self.avg_season_rank = 0
        self.avg_draft_pick = 0

        # Cumulative counters for how many times a team reached each playoff round
        self.playoff_round_1 = 0   # Number of times reached round 1
        self.playoff_round_2 = 0   # Number of times reached round 2
        self.playoff_round_3 = 0   # Number of times reached round 3
        self.playoff_final = 0     # Number of times reached the final
        self.playoff_championship = 0  # Number of times won the championship


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
            self.avg_tickets = (self.avg_tickets * (self.total_seasons_played - 1) + self.tickets)  / self.total_seasons_played # if made to play off add 0 to avg tickets
            self.avg_strength = (self.avg_strength * (self.total_seasons_played - 1) + self.strength)  / self.total_seasons_played
            self.avg_season_rank = (self.avg_season_rank * (self.total_seasons_played - 1) + self.season_rank) / self.total_seasons_played
            self.avg_draft_pick = (self.avg_draft_pick * (self.total_seasons_played - 1) + self.season_draft_pick) / self.total_seasons_played


    def update_strength(self):

        # Decrease team strength after the season (players got old, etc.)
        decay = random.uniform(MIN_TEAM_STRENGTH_DECREASE, MAX_TEAM_STRENGTH_DECREASE) 
        self.strength *= (1 - decay)

        # 2. Draft pick boost (absolute gain from draft)
        coef = DRAFT_PICK_STRENGTH.get(self.season_draft_pick, 
                                       random.uniform(DRAFT_PICK_STRENGTH.get(13), DRAFT_PICK_STRENGTH.get(14)))
        draft_boost = coef * (MAX_POSSIBLE_TEAM_STRENGTH - self.strength) * DRAFT_BOOST_COEF
        self.strength += draft_boost

        self.strength = min(MAX_POSSIBLE_TEAM_STRENGTH, round(self.strength, 2))


    def update_playoff_rounds(self):
        rank = self.playoff_rank

        if rank == -1:
            # Did not make playoffs
            return

        if rank >= 0:
            self.playoff_round_1 += 1
        if rank >= 1:
            self.playoff_round_2 += 1
        if rank >= 2:
            self.playoff_round_3 += 1
        if rank >= 3:
            self.playoff_final += 1
        if rank == 4:
            self.playoff_championship += 1




    def end_season(self):
        # Add season results to totals
        self.total_wins += self.season_wins
        self.total_loses += self.season_loses
        self.total_games += self.season_games
        self.total_seasons_played += 1

        # Update averages
        self.update_averages()
        self.update_playoff_rounds()


        


    def __str__(self):
        return (
            f"Team: {self.name}\n"
            f"  Strength: {self.strength:.2f}\n"
            f"  tickets: {self.tickets:.2f}\n"
            f"  Season: {self.season_wins}-{self.season_loses} "
            f"(Games: {self.season_games}, Rank: {self.season_rank})\n"
            f"  Playoff Rank: {self.playoff_rank}\n"
            f"  Total: {self.total_wins}-{self.total_loses} "
            f"(Games: {self.total_games}, Seasons: {self.total_seasons_played})\n"
            f"  Draft Pick: {self.season_draft_pick}\n"
            f"  --- Averages ---\n"
            f"  Avg Season Wins: {self.avg_season_wins:.2f}\n"
            f"  Avg tickets: {self.avg_tickets:.2f}\n"
            f"  Avg Strength: {self.avg_strength:.2f}\n"
            f"  Avg Season Rank: {self.avg_season_rank:.2f}\n"
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
            "tickets": self.tickets,
            "strength": self.strength,
            "season_draft_pick": self.season_draft_pick,
            "total_seasons_played": self.total_seasons_played,
            "avg_season_wins": self.avg_season_wins,
            "avg_tickets": self.avg_tickets,
            "avg_strength": self.avg_strength,
            "avg_season_rank": self.avg_season_rank,
            "avg_draft_pick": self.avg_draft_pick,

            # New playoff round fields
            "playoff_round_1": self.playoff_round_1,
            "playoff_round_2": self.playoff_round_2,
            "playoff_round_3": self.playoff_round_3,
            "playoff_final": self.playoff_final,
            "playoff_championship": self.playoff_championship
        }
    



import random
import itertools
from typing import List

from code.constants import MIN_TEAM_STRENGTH, MAX_TEAM_STRENGTH, TEAM_NAME_MAP, GAMES_PER_TEAM_REGULAR_SEASON, MIN_NUMBER_OF_GAMES_BETWEEN_TWO_TEAMS
from .team import Team
from code.coincalc import apply_rank_penalty, apply_draft_penalty


# initialize teams for simulation
def initialize_teams(num_teams):
    # Get unique team names
    unique_names = list(set(TEAM_NAME_MAP.values()))

    if num_teams > len(unique_names):
        raise ValueError(f"Requested {num_teams} teams, but only {len(unique_names)} unique team names available.")

    # Shuffle to randomize selection (optional)
    random.shuffle(unique_names)

    # Select first num_teams names
    selected_names = unique_names[:num_teams]

    # Initialize teams (here, just returning names; replace with Team() if you have a class)
    teams = []
    for name in selected_names:
        strength = random.randint(MIN_TEAM_STRENGTH, MAX_TEAM_STRENGTH)
        team = Team(name=name, strength=strength)
        teams.append(team)

    return teams


# Simulation of the game
def simulate_game(team1: Team, team2: Team, playoff = False):
    total_strength = team1.strength + team2.strength
    prob_team1_wins = team1.strength / total_strength

    if random.random() < prob_team1_wins:
        winner, loser = team1, team2
    else:
        winner, loser = team2, team1

    if not playoff:
        # Update season stats
        winner.season_wins += 1
        winner.season_games += 1
        loser.season_loses += 1
        loser.season_games += 1

        # Update total stats
        winner.total_wins += 1
        winner.total_games += 1
        loser.total_loses += 1
        loser.total_games += 1


# simulate regular season
def regular_season_simulate(teams: List[Team]):

    # Assign variables
    num_teams = len(teams)
    target_games_per_team = round(GAMES_PER_TEAM_REGULAR_SEASON * (num_teams - 1))

    # Simulate traget games per pair (just duplicates of the pair)
    all_pairs = list(itertools.combinations(teams, 2))
    for pair in all_pairs:
        for _ in range(MIN_NUMBER_OF_GAMES_BETWEEN_TWO_TEAMS):
            simulate_game(pair[0], pair[1])
    
    # Simulate extra random games between random pairs until each team reaches target
    while any(team.season_games < target_games_per_team for team in teams):
        # Filter only valid pairs where both teams still need games
        eligible_pairs = [
            pair for pair in all_pairs
            if pair[0].season_games < target_games_per_team and pair[1].season_games < target_games_per_team
        ]
        
        if not eligible_pairs:
            # No more valid pairs to add — break to avoid infinite loop
            break

        # Randomly pick one eligible pair
        pair = random.choice(eligible_pairs)

        simulate_game(pair[0], pair[1])
        

def simulate_playoff_round(team1: Team, team2: Team) -> Team:
    wins1 = 0
    wins2 = 0
    while wins1 < 4 and wins2 < 4:
        winner = simulate_game(team1, team2, playoff=True)
        if winner == team1:
            wins1 += 1
        else:
            wins2 += 1
  
    return team1 if wins1 == 4 else team2


# simulate playoff games
def playoff_simulate(teams: List[Team]):

    if (len(teams) < 20):
        print(f"Teams list has less than 20 teams, min 20 teams is required")
        return
    
    teams_sorted = sorted(teams, key=lambda team: team.season_wins, reverse = True)
    # select teams for playoff
    teams_playoff = teams_sorted[:16]

    # First round matchups: 1 vs 16, 2 vs 15
    round_teams = []
    for i in range(len(teams_playoff) // 2):
        high = teams_playoff[i]
        low = teams_playoff[-(i+1)]

        #set rank to 0 since both of them made it to playoffs
        high.playoff_rank, low.playoff_rank = 0, 0

        winner = simulate_playoff_round(high, low)
        #update the rank of the winner
        winner.playoff_rank += 1
        round_teams.append(winner)

    # Continue until we have a champion
    while len(round_teams) > 1:
        next_round = []
        for i in range(0, len(round_teams), 2):
            winner = simulate_playoff_round(round_teams[i], round_teams[i+1])
            winner.playoff_rank += 1
            next_round.append(winner)
        round_teams = next_round


# update coins after season    
def coins_after_season(teams: List[Team]):
    for team in teams:
        team.coins = apply_rank_penalty(team.coins, team.playoff_rank)


# simulate the draft process
def draft_simulate(teams: List[Team], picks=4):
    # Copy list to avoid modifying the original
    draft_pool = teams[:]

    for i in range(picks + 1):
        if not draft_pool:
            break
        # Build weighted choices
        weights = [team.coins for team in draft_pool]
        chosen = random.choices(draft_pool, weights=weights, k=1)[0]
        chosen.season_draft_pick = i
        draft_pool.remove(chosen)


# update coins after draft
def coins_after_draft(teams: List[Team]):
    for team in teams:
        team.coins = apply_draft_penalty(team.coins, team.season_draft_pick)
    


    



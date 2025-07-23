import random
import itertools
from typing import List

from code.constants import MIN_TEAM_STRENGTH, MAX_TEAM_STRENGTH, TEAM_NAME_MAP, GAMES_PER_TEAM_REGULAR_SEASON, MIN_NUMBER_OF_GAMES_BETWEEN_TWO_TEAMS
from team import Team


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
def simulate_game(team1: Team, team2: Team):
    total_strength = team1.strength + team2.strength
    prob_team1_wins = team1.strength / total_strength

    if random.random() < prob_team1_wins:
        winner, loser = team1, team2
    else:
        winner, loser = team2, team1

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
def regular_season_simulated(teams: List[Team]):

    # Assign variables
    num_teams = len(teams)
    target_games_per_team = round(GAMES_PER_TEAM_REGULAR_SEASON * (num_teams - 1))

    # Simulate traget games per pair (just duplicates of the pair)
    all_pairs = list(itertools.combinations(teams, 2))
    schedule = []
    for pair in all_pairs:
        for _ in range(MIN_NUMBER_OF_GAMES_BETWEEN_TWO_TEAMS):
            simulate_game(pair)
    
    
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

        simulate_game(pair)
        


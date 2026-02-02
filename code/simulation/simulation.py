import random
import itertools
from typing import List

from code.constants import DRAFT_PICK_STRENGTH, MIN_TEAM_STRENGTH, MAX_TEAM_STRENGTH, TEAM_NAME_MAP, GAMES_PER_TEAM_REGULAR_SEASON, MIN_NUMBER_OF_GAMES_BETWEEN_TWO_TEAMS
from .team import Team
from code.coincalc import apply_rank_penalty, apply_draft_penalty


# initialize teams for simulation
def initialize_teams(num_teams) -> List[Team]:
    # Get unique team names
    unique_names = list(set(TEAM_NAME_MAP.values()))

    if num_teams > len(unique_names):
        raise ValueError(f"Requested {num_teams} teams, but only {len(unique_names)} unique team names available.")

    # Shuffle to randomize selection (optional)
    random.shuffle(unique_names)

    # Select first num_teams names
    selected_names = [str(i) for i in range(1, num_teams + 1)]#unique_names[:num_teams]

    # Initialize teams (here, just returning names; replace with Team() if you have a class)
    teams = []
    for name in selected_names:
        # random strength
        strength = random.randint(MIN_TEAM_STRENGTH, MAX_TEAM_STRENGTH)

        # Normalize weakness (higher = weaker team)
        weakness = MAX_TEAM_STRENGTH - strength + 1  
        # Add randomness but bias toward weakness
        lottery_index = random.randint(1, weakness * 2) * 10

        team = Team(name=name, strength=strength, lottery_index=lottery_index)
        teams.append(team)

    return teams

def spread_strength(teams):
    num_teams = len(teams)

    # Step 1: generate random numbers for desired spread
    raw_strengths = [random.uniform(MIN_TEAM_STRENGTH, MAX_TEAM_STRENGTH) for _ in range(num_teams)]
    min_rand = min(raw_strengths)
    max_rand = max(raw_strengths)

    # get the old min and max from the current team strengths
    old_strengths = [t.strength for t in teams]
    old_min = min(old_strengths)
    old_max = max(old_strengths)

    # Step 3: linearly scale each team to the new min/max range
    for t in teams:
        pct = (t.strength - old_min) / (old_max - old_min)  # position in old range
        t.strength = pct * (max_rand - min_rand) + min_rand  # map to new range


# Simulation of the game
def simulate_game(team1: Team, team2: Team, target_num_of_games = None):
    total_strength = team1.strength + team2.strength
    prob_team1_wins = team1.strength / total_strength

    if random.random() < prob_team1_wins:
        winner, loser = team1, team2
    else:
        winner, loser = team2, team1

    # for simulations, sometimes we have no pairs left, so one team has less then target amount of games
    if target_num_of_games:
        if winner.season_games < target_num_of_games:
            winner.season_wins += 1
            winner.season_games += 1
        if loser.season_games < target_num_of_games:
            loser.season_loses += 1
            loser.season_games += 1

    return winner



# simulate regular season
def regular_season_simulate(teams: List[Team]):

    # Assign variables
    num_teams = len(teams)
    target_games_per_team = round(GAMES_PER_TEAM_REGULAR_SEASON * (num_teams - 1))

    # Simulate traget games per pair (just duplicates of the pair)
    all_pairs = list(itertools.combinations(teams, 2))
    for pair in all_pairs:
        for _ in range(MIN_NUMBER_OF_GAMES_BETWEEN_TWO_TEAMS):
            simulate_game(pair[0], pair[1], target_games_per_team)
    
    # Simulate extra random games between random pairs until each team reaches target
    while any(team.season_games < target_games_per_team for team in teams):
        # Filter only valid pairs where both teams still need games
        eligible_pairs = [
            pair for pair in all_pairs
            if pair[0].season_games < target_games_per_team or pair[1].season_games < target_games_per_team
        ]
        
        if not eligible_pairs:
            # No more valid pairs to add — break to avoid infinite loop
            break

        # Randomly pick one eligible pair
        pair = random.choice(eligible_pairs)

        simulate_game(pair[0], pair[1], target_games_per_team)

    teams_sorted = sorted(teams, key=lambda team: team.season_wins, reverse = True)
    for i in range(num_teams):
        teams_sorted[i].season_rank = i + 1
    

def simulate_playoff_round(team1: Team, team2: Team) -> Team:
    wins1 = 0
    wins2 = 0
    while wins1 < 4 and wins2 < 4:
        winner = simulate_game(team1, team2)
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


# update lottery_index after season    
def lottery_index_after_season(teams: List[Team]):
    for team in teams:
        team.lottery_index = apply_rank_penalty(team.lottery_index, team.playoff_rank)


# simulate the draft process
def draft_simulate(teams: List[Team]):
    # Split teams into non-playoff and playoff groups
    non_playoff_teams = [team for team in teams if team.playoff_rank == -1]
    playoff_teams = [team for team in teams if team.playoff_rank != -1]

    # -------------------------------
    # Step 1: Lottery for non-playoff teams
    # -------------------------------
    draft_pool = non_playoff_teams[:]
    picks = len(DRAFT_PICK_STRENGTH)  # first 14 picks

    for i in range(picks):
        if not draft_pool:
            break
        # Weighted choice based on lottery_index
        weights = [team.lottery_index for team in draft_pool]
        chosen = random.choices(draft_pool, weights=weights, k=1)[0]
        chosen.season_draft_pick = i + 1
        draft_pool.remove(chosen)

    # -------------------------------
    # Step 2: Assign remaining picks
    # Non-picked non-playoff teams + playoff teams
    # -------------------------------
    remaining_teams = draft_pool + playoff_teams
    random.shuffle(remaining_teams)
    for team in remaining_teams:
        picks += 1
        team.season_draft_pick = picks


# update lottery_index after draft
def lottery_index_after_draft(teams: List[Team]):
    for team in teams:
        team.lottery_index = apply_draft_penalty(team.lottery_index, team.season_draft_pick)
    

def end_season(teams: List[Team]):
    for team in teams:
        team.end_season()


    



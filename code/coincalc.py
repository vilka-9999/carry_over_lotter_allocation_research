import pandas as pd
import re

from .constants import FIRST_PICK_COINS_COEF, SECOND_PICK_COINS_COEF, THIRD_PICK_COINS_COEF, FOURTH_PICK_COINS_COEF, NO_PLAYOFFS_BONUS, ROUND_1_LOSS_COEF, ROUND_2_LOSS_COEF, ROUND_3_LOSS_COEF, FINAL_LOSS_COEF, CHAMPION_COEF


# === Penalty functions ===
# These functions calculate the new coin total based on the current coins
# and the specific event (draft pick or playoff rank).

def apply_draft_penalty(coins, pick):
    """
    Applies a penalty to coins based on the draft pick position.
    Coins will always be rounded to an integer.
    """
    if pick == 1:
        result = coins * FIRST_PICK_COINS_COEF  # 1st pick: coins reset to 0
    elif pick == 2:
        result = coins * SECOND_PICK_COINS_COEF  # 2nd pick: lose 75%
    elif pick == 3:
        result = coins * THIRD_PICK_COINS_COEF   # 3rd pick: lose 50%
    elif pick == 4:
        result = coins * FOURTH_PICK_COINS_COEF  # 4th pick: lose 25%
    else:
        result = coins  # No penalty

    return int(round(result))  # round to nearest integer


def apply_rank_penalty(coins, rank):
    """
    Applies a penalty or bonus based on playoff rank.
    Coins will always be rounded to an integer.
    """
    if rank == -1:
        result = coins + NO_PLAYOFFS_BONUS  # Didn't make playoffs: +1 coin
    elif rank == 0:
        result = coins * ROUND_1_LOSS_COEF    # Lost in 1st round
    elif rank == 1:
        result = coins * ROUND_2_LOSS_COEF   # Lost in 2nd round
    elif rank == 2:
        result = coins * ROUND_3_LOSS_COEF   # Lost in 3rd round
    elif rank == 3:
        result = coins * FINAL_LOSS_COEF     # Lost in final
    elif rank == 4:
        result = coins * CHAMPION_COEF       # Won final
    else:
        result = coins

    return int(round(result))  # round to nearest integer


# === CALCULATIONS BASED ON HISTORICAL DATA ===
def coincalc_history():
    # === Load Excel files ===

    playoff_df = pd.read_csv('data/TeamsRank_1985-2024.csv')

    draft_df = pd.read_csv('data/DraftPicks_1985-2024.csv')

    # Sort data by normalized team name and year to ensure chronological processing
    playoff_df = playoff_df.sort_values(by=["team_normalized", "year"])
    draft_df = draft_df.sort_values(by=["pick_team_normalized", "year"])


    # === Calculate coins for each team ===
    columns = ['year', 'team_normalized', 'coins']
    rows = []

    # Iterate through each normalized team found in the playoff data
    for team_normalized in playoff_df['team_normalized'].unique():
        # Get all historical data for the current normalized team, sorted by year
        team_playoff_data = playoff_df[playoff_df['team_normalized'] == team_normalized].sort_values(by='year')
        coins = 0 # Initialize coins for the current team for the calculation for this team's history

        # Check if team_playoff_data is empty before accessing .iloc[0]
        if team_playoff_data.empty:
            print(f"Skipping empty playoff data for normalized team: {team_normalized}")
            continue
            
        original_team_name = team_playoff_data['team'].iloc[0]

        print(f"\n--- Calculating coins for {original_team_name} (Normalized: {team_normalized}) ---")

        # Iterate through each year's performance for the team 
        for _, row in team_playoff_data.iterrows():
            year = row['year']
            rank = row['rank_playoffs']
            
            coins_before_rank = coins # Store coins before rank penalty 
        
            coins = apply_rank_penalty(coins, rank)
            print(f"  {year}: Rank = {rank}, Coins before rank penalty: {coins_before_rank:.2f}, After rank penalty: {coins:.2f}")

            
            draft_row_for_team = draft_df[
                (draft_df['pick_team_normalized'] == team_normalized) &
                (draft_df['year'] == year)
            ]

            if not draft_row_for_team.empty:
                pick = draft_row_for_team.iloc[0]['pick']
            
                if pd.isna(pick) or not (1 <= pick <= 4): 
                    print(f"    Warning: Draft pick for {original_team_name} in {year} is missing or invalid ({pick}). Skipping draft penalty.")
                else:
                    coins_before_draft = coins 
                    coins = apply_draft_penalty(coins, pick)
                    print(f"    -> Draft pick found (Pick {pick}). Coins before draft penalty: {coins_before_draft:.2f}, After draft penalty: {coins:.2f}")
            else:
                print(f"    -> No top-4 draft pick found for {original_team_name} in {year}.")

            print(f"  {year}: Final coins for year: {coins:.2f}")

            rows.append([year, team_normalized, round(coins, 2)])


    print("\n=== Creating DB ===")

    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(f'results/coins_based_on_existing_results.csv')


    






def main():
    coincalc_history()

if __name__ == '__main__':
    main()











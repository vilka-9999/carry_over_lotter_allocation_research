import pandas as pd
import re

from .constants import FIRST_PICK_LOTTERY_INDEX_COEF, SECOND_PICK_LOTTERY_INDEX_COEF, THIRD_PICK_LOTTERY_INDEX_COEF, FOURTH_PICK_LOTTERY_INDEX_COEF, NO_PLAYOFFS_BONUS, ROUND_1_LOSS_COEF, ROUND_2_LOSS_COEF, ROUND_3_LOSS_COEF, FINAL_LOSS_COEF, CHAMPION_COEF


# === Penalty functions ===
# These functions calculate the new coin total based on the current lottery_index
# and the specific event (draft pick or playoff rank).

def apply_draft_penalty(lottery_index, pick):
    """
    Applies a penalty to lottery_index based on the draft pick position.
    lottery_index will always be rounded to an integer.
    """
    if pick == 1:
        result = lottery_index * FIRST_PICK_LOTTERY_INDEX_COEF  # 1st pick: lottery_index reset to 0
    elif pick == 2:
        result = lottery_index * SECOND_PICK_LOTTERY_INDEX_COEF  # 2nd pick: lose 75%
    elif pick == 3:
        result = lottery_index * THIRD_PICK_LOTTERY_INDEX_COEF   # 3rd pick: lose 50%
    elif pick == 4:
        result = lottery_index * FOURTH_PICK_LOTTERY_INDEX_COEF  # 4th pick: lose 25%
    else:
        result = lottery_index  # No penalty

    return int(round(result))  # round to nearest integer


def apply_rank_penalty(lottery_index, rank):
    """
    Applies a penalty or bonus based on playoff rank.
    lottery_index will always be rounded to an integer.
    """
    if rank == -1:
        result = lottery_index + NO_PLAYOFFS_BONUS  # Didn't make playoffs: +1 coin
    elif rank == 0:
        result = lottery_index * ROUND_1_LOSS_COEF    # Lost in 1st round
    elif rank == 1:
        result = lottery_index * ROUND_2_LOSS_COEF   # Lost in 2nd round
    elif rank == 2:
        result = lottery_index * ROUND_3_LOSS_COEF   # Lost in 3rd round
    elif rank == 3:
        result = lottery_index * FINAL_LOSS_COEF     # Lost in final
    elif rank == 4:
        result = lottery_index * CHAMPION_COEF       # Won final
    else:
        result = lottery_index

    return int(round(result))  # round to nearest integer


# === CALCULATIONS BASED ON HISTORICAL DATA ===
def lottery_indexcalc_history():
    # === Load Excel files ===

    playoff_df = pd.read_csv('data/TeamsRank_1985-2024.csv')

    draft_df = pd.read_csv('data/DraftPicks_1985-2024.csv')

    # Sort data by normalized team name and year to ensure chronological processing
    playoff_df = playoff_df.sort_values(by=["team_normalized", "year"])
    draft_df = draft_df.sort_values(by=["pick_team_normalized", "year"])


    # === Calculate lottery_index for each team ===
    columns = ['year', 'team_normalized', 'lottery_index']
    rows = []

    # Iterate through each normalized team found in the playoff data
    for team_normalized in playoff_df['team_normalized'].unique():
        # Get all historical data for the current normalized team, sorted by year
        team_playoff_data = playoff_df[playoff_df['team_normalized'] == team_normalized].sort_values(by='year')
        lottery_index = 0 # Initialize lottery_index for the current team for the calculation for this team's history

        # Check if team_playoff_data is empty before accessing .iloc[0]
        if team_playoff_data.empty:
            print(f"Skipping empty playoff data for normalized team: {team_normalized}")
            continue
            
        original_team_name = team_playoff_data['team'].iloc[0]

        print(f"\n--- Calculating lottery_index for {original_team_name} (Normalized: {team_normalized}) ---")

        # Iterate through each year's performance for the team 
        for _, row in team_playoff_data.iterrows():
            year = row['year']
            rank = row['rank_playoffs']
            
            lottery_index_before_rank = lottery_index # Store lottery_index before rank penalty 
        
            lottery_index = apply_rank_penalty(lottery_index, rank)
            print(f"  {year}: Rank = {rank}, lottery_index before rank penalty: {lottery_index_before_rank:.2f}, After rank penalty: {lottery_index:.2f}")

            
            draft_row_for_team = draft_df[
                (draft_df['pick_team_normalized'] == team_normalized) &
                (draft_df['year'] == year)
            ]

            if not draft_row_for_team.empty:
                pick = draft_row_for_team.iloc[0]['pick']
            
                if pd.isna(pick) or not (1 <= pick <= 4): 
                    print(f"    Warning: Draft pick for {original_team_name} in {year} is missing or invalid ({pick}). Skipping draft penalty.")
                else:
                    lottery_index_before_draft = lottery_index 
                    lottery_index = apply_draft_penalty(lottery_index, pick)
                    print(f"    -> Draft pick found (Pick {pick}). lottery_index before draft penalty: {lottery_index_before_draft:.2f}, After draft penalty: {lottery_index:.2f}")
            else:
                print(f"    -> No top-4 draft pick found for {original_team_name} in {year}.")

            print(f"  {year}: Final lottery_index for year: {lottery_index:.2f}")

            rows.append([year, team_normalized, round(lottery_index, 2)])


    print("\n=== Creating DB ===")

    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(f'results/lottery_index_based_on_existing_results.csv')


    






def main():
    lottery_indexcalc_history()

if __name__ == '__main__':
    main()











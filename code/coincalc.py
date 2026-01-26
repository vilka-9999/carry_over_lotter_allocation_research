import pandas as pd
import re

from .constants import FIRST_PICK_TICKETS_COEF, SECOND_PICK_TICKETS_COEF, THIRD_PICK_TICKETS_COEF, FOURTH_PICK_TICKETS_COEF, NO_PLAYOFFS_BONUS, ROUND_1_LOSS_COEF, ROUND_2_LOSS_COEF, ROUND_3_LOSS_COEF, FINAL_LOSS_COEF, CHAMPION_COEF


# === Penalty functions ===
# These functions calculate the new coin total based on the current tickets
# and the specific event (draft pick or playoff rank).

def apply_draft_penalty(tickets, pick):
    """
    Applies a penalty to tickets based on the draft pick position.
    tickets will always be rounded to an integer.
    """
    if pick == 1:
        result = tickets * FIRST_PICK_TICKETS_COEF  # 1st pick: tickets reset to 0
    elif pick == 2:
        result = tickets * SECOND_PICK_TICKETS_COEF  # 2nd pick: lose 75%
    elif pick == 3:
        result = tickets * THIRD_PICK_TICKETS_COEF   # 3rd pick: lose 50%
    elif pick == 4:
        result = tickets * FOURTH_PICK_TICKETS_COEF  # 4th pick: lose 25%
    else:
        result = tickets  # No penalty

    return int(round(result))  # round to nearest integer


def apply_rank_penalty(tickets, rank):
    """
    Applies a penalty or bonus based on playoff rank.
    tickets will always be rounded to an integer.
    """
    if rank == -1:
        result = tickets + NO_PLAYOFFS_BONUS  # Didn't make playoffs: +1 coin
    elif rank == 0:
        result = tickets * ROUND_1_LOSS_COEF    # Lost in 1st round
    elif rank == 1:
        result = tickets * ROUND_2_LOSS_COEF   # Lost in 2nd round
    elif rank == 2:
        result = tickets * ROUND_3_LOSS_COEF   # Lost in 3rd round
    elif rank == 3:
        result = tickets * FINAL_LOSS_COEF     # Lost in final
    elif rank == 4:
        result = tickets * CHAMPION_COEF       # Won final
    else:
        result = tickets

    return int(round(result))  # round to nearest integer


# === CALCULATIONS BASED ON HISTORICAL DATA ===
def ticketscalc_history():
    # === Load Excel files ===

    playoff_df = pd.read_csv('data/TeamsRank_1985-2024.csv')

    draft_df = pd.read_csv('data/DraftPicks_1985-2024.csv')

    # Sort data by normalized team name and year to ensure chronological processing
    playoff_df = playoff_df.sort_values(by=["team_normalized", "year"])
    draft_df = draft_df.sort_values(by=["pick_team_normalized", "year"])


    # === Calculate tickets for each team ===
    columns = ['year', 'team_normalized', 'tickets']
    rows = []

    # Iterate through each normalized team found in the playoff data
    for team_normalized in playoff_df['team_normalized'].unique():
        # Get all historical data for the current normalized team, sorted by year
        team_playoff_data = playoff_df[playoff_df['team_normalized'] == team_normalized].sort_values(by='year')
        tickets = 0 # Initialize tickets for the current team for the calculation for this team's history

        # Check if team_playoff_data is empty before accessing .iloc[0]
        if team_playoff_data.empty:
            print(f"Skipping empty playoff data for normalized team: {team_normalized}")
            continue
            
        original_team_name = team_playoff_data['team'].iloc[0]

        print(f"\n--- Calculating tickets for {original_team_name} (Normalized: {team_normalized}) ---")

        # Iterate through each year's performance for the team 
        for _, row in team_playoff_data.iterrows():
            year = row['year']
            rank = row['rank_playoffs']
            
            tickets_before_rank = tickets # Store tickets before rank penalty 
        
            tickets = apply_rank_penalty(tickets, rank)
            print(f"  {year}: Rank = {rank}, tickets before rank penalty: {tickets_before_rank:.2f}, After rank penalty: {tickets:.2f}")

            
            draft_row_for_team = draft_df[
                (draft_df['pick_team_normalized'] == team_normalized) &
                (draft_df['year'] == year)
            ]

            if not draft_row_for_team.empty:
                pick = draft_row_for_team.iloc[0]['pick']
            
                if pd.isna(pick) or not (1 <= pick <= 4): 
                    print(f"    Warning: Draft pick for {original_team_name} in {year} is missing or invalid ({pick}). Skipping draft penalty.")
                else:
                    tickets_before_draft = tickets 
                    tickets = apply_draft_penalty(tickets, pick)
                    print(f"    -> Draft pick found (Pick {pick}). tickets before draft penalty: {tickets_before_draft:.2f}, After draft penalty: {tickets:.2f}")
            else:
                print(f"    -> No top-4 draft pick found for {original_team_name} in {year}.")

            print(f"  {year}: Final tickets for year: {tickets:.2f}")

            rows.append([year, team_normalized, round(tickets, 2)])


    print("\n=== Creating DB ===")

    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(f'results/tickets_based_on_existing_results.csv')


    






def main():
    ticketscalc_history()

if __name__ == '__main__':
    main()











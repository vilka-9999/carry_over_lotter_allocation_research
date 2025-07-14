import pandas as pd
import re

team_name_map = {
    "atlanta hawks": "atlanta hawks",
    "boston celtics": "boston celtics",
    "brooklyn nets": "brooklyn nets",
    "new jersey nets": "brooklyn nets", 
    "charlotte hornets": "charlotte hornets",
    "charlotte bobcats": "charlotte hornets", 
    "chicago bulls": "chicago bulls",
    "cleveland cavaliers": "cleveland cavaliers",
    "dallas mavericks": "dallas mavericks",
    "denver nuggets": "denver nuggets",
    "detroit pistons": "detroit pistons",
    "golden state warriors": "golden state warriors",
    "houston rockets": "houston rockets",
    "indiana pacers": "indiana pacers",
    "los angeles clippers": "los angeles clippers",
    "san diego clippers": "los angeles clippers", 
    "los angeles lakers": "los angeles lakers",
    "memphis grizzlies": "memphis grizzlies",
    "vancouver grizzlies": "memphis grizzlies",
    "miami heat": "miami heat",
    "milwaukee bucks": "milwaukee bucks",
    "minnesota timberwolves": "minnesota timberwolves",
    "new orleans pelicans": "new orleans pelicans",
    "new orleans hornets": "new orleans pelicans", 
    "new orleansoklahoma city hornets": "new orleans pelicans", 
    "new york knicks": "new york knicks",
    "oklahoma city thunder": "oklahoma city thunder",
    "seattle supersonics": "oklahoma city thunder",
    "orlando magic": "orlando magic",
    "philadelphia 76ers": "philadelphia 76ers",
    "philadelphia ers": "philadelphia 76ers", 
    "philadelphia sixers": "philadelphia 76ers", 
    "phoenix suns": "phoenix suns",
    "portland trail blazers": "portland trail blazers",
    "sacramento kings": "sacramento kings",
    "kansas city kings": "sacramento kings", 
    "san antonio spurs": "san antonio spurs",
    "toronto raptors": "toronto raptors",
    "utah jazz": "utah jazz",
    "washington wizards": "washington wizards",
    "washington bullets": "washington wizards",
}


def normalize_team_name(team_name):
    """
    Normalizes team names using a predefined mapping.
    Converts input team names to lowercase and strips whitespace
    before looking them up in the mapping.
    """
    if isinstance(team_name, str):
        # Convert to lowercase 
        lower_name = team_name.lower().strip()
        # Return the name if found.
        # If not found in the map, return the lowercase
        return team_name_map.get(lower_name, lower_name)
    return team_name # Return as is if not a string (e.g., NaN, None)


# === Load Excel files ===
try:
    playoff_df = pd.read_excel("playoff_data.xlsx", header=1)
    playoff_df.columns = playoff_df.columns.str.strip()
    # Apply normalization to team names in playoff_df
    playoff_df['team_normalized'] = playoff_df['team'].apply(normalize_team_name)
    playoff_df['year'] = playoff_df['year'].astype(int)
except FileNotFoundError:
    print("Error: 'playoff_data.xlsx' not found. Please ensure the file is in the correct directory.")
    exit() # Exit if a crucial file is missing

try:
    draft_df = pd.read_excel("draft_data.xlsx", header=1)
    draft_df.columns = draft_df.columns.str.strip()
    # Apply normalization to team names in draft_df
    draft_df['pick_team_normalized'] = draft_df['pick_team'].apply(normalize_team_name)
    draft_df['year'] = draft_df['year'].astype(int)
except FileNotFoundError:
    print("Error: 'draft_data.xlsx' not found. Please ensure the file is in the correct directory.")
    exit() # Exit if a crucial file is missing

# Sort data by normalized team name and year to ensure chronological processing
playoff_df = playoff_df.sort_values(by=["team_normalized", "year"])
draft_df = draft_df.sort_values(by=["pick_team_normalized", "year"])

# === Penalty functions ===
# These functions calculate the new coin total based on the current coins
# and the specific event (draft pick or playoff rank).

def apply_draft_penalty(coins, pick):
    """
    Applies a penalty to coins based on the draft pick position.
    This penalty is applied *after* the rank penalty for the year.
    """
    if pick == 1:
        return 0  # 1st pick: coins reset to 0
    elif pick == 2:
        return coins * 0.25 # 2nd pick: lose 75%
    elif pick == 3:
        return coins * 0.5  # 3rd pick: lose 50%
    elif pick == 4:
        return coins * 0.75 # 4th pick: lose 25%
    return coins # No penalty for picks outside top 4

def apply_rank_penalty(coins, rank):
    """
    Applies a penalty or bonus to coins based on the team's playoff rank.
    This is the first calculation applied for each year.
    """
    if rank == -1:
        return coins + 1 # Didn't make playoffs: +1 coin
    elif rank == 0:
        return coins     # Lost in 1st round: coins remain unchanged
    elif rank == 1:
        return coins * 0.75 # Lost in 2nd round: lose 25%, keep 75%
    elif rank == 2:
        return coins * 0.5  # Lost in 3rd round: lose 50%, keep 50%
    elif rank == 3:
        return coins * 0.25 # Lost in the final: lose 75%, keep 25%
    elif rank == 4:
        return 0            # Won the final: coins reset to 0
    return coins # Return current coins if rank is not recognized

# === Calculate coins for each team ===
team_coins = {} # Dictionary to store final coin totals for each team

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
        rank = row['rank']
        
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

      
        coins = round(coins, 2)
        print(f"  {year}: Final coins for year: {coins:.2f}")

    team_coins[original_team_name] = coins


print("\n=== Final Coin Totals ===")

for team, coins in sorted(team_coins.items(), key=lambda x: -x[1]):
    print(f"{team}: {coins} coins")







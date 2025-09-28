
from .simulation import initialize_teams, regular_season_simulate, playoff_simulate, coins_after_season, coins_after_draft, draft_simulate, end_season
import pandas as pd

output_file = 'results/simulation_results.csv'
teams = initialize_teams(30)
for i in range(1000):
    print(f'Simulating season {i}')
    regular_season_simulate(teams)
    playoff_simulate(teams)
    coins_after_season(teams)
    draft_simulate(teams)
    coins_after_draft(teams)
    end_season(teams)

    '''# Convert to DataFrame
    df = pd.DataFrame([team.to_dict() for team in teams])
    
    # Add season number column
    df.insert(0, 'season', i)
    
    # Write / append to CSV
    if i == 0:
        df.to_csv(output_file, index=False)  # write header
    else:
        df.to_csv(output_file, mode='a', index=False, header=False)  # append without header'''

    if i == 1000 - 1:
        df = pd.DataFrame([team.to_dict() for team in teams])
        df.to_csv(output_file, index=False) 

    for team in teams:
        team.clear_season_stats()
        team.update_strength()

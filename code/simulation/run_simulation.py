
from .simulation import initialize_teams, regular_season_simulate

teams = initialize_teams(6)
regular_season_simulate(teams)
print(teams)
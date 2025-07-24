
from .simulation import initialize_teams, regular_season_simulate, playoff_simulate, coins_after_season, coins_after_draft, draft_simulate

teams = initialize_teams(30)
regular_season_simulate(teams)
playoff_simulate(teams)
coins_after_season(teams)
draft_simulate(teams)
coins_after_draft(teams)
print(teams)
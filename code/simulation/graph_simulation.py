from .simulation import spread_strength, initialize_teams, regular_season_simulate, playoff_simulate, lottery_index_after_season, lottery_index_after_draft, draft_simulate, end_season
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import copy


def graph1000(columns):
    output_file = 'results/simulation_1000_results.csv'

    # -------------------------------
    # Simulation parameters
    # -------------------------------
    num_teams = 30
    num_seasons = 1000

    # -------------------------------
    # Initialize teams
    # -------------------------------
    teams = initialize_teams(num_teams)

    # -------------------------------
    # Run simulation
    # -------------------------------
    for season in range(1, num_seasons + 1):
        print(f"Simulating season {season+1}/{num_seasons}")

        # uniform strength spread
        spread_strength(teams)

        # Regular season and playoffs
        regular_season_simulate(teams)
        playoff_simulate(teams)

        # Update lottery_index and draft
        lottery_index_after_season(teams)
        draft_simulate(teams)
        lottery_index_after_draft(teams)

        # End season (updates totals and averages)
        end_season(teams)

        if season == num_seasons: # save last season stats for a file
            df = pd.DataFrame([team.to_dict() for team in teams])
            df.to_csv(output_file, index=False)

            # -------------------------------
            # Create DataFrame with averages
            # -------------------------------
            df = pd.DataFrame([team.to_dict() for team in teams])

            # -------------------------------
            # One chart per column
            # -------------------------------
            for col in columns:

                plt.figure(figsize=(18, 7))

                plt.bar(
                    df["name"],
                    df[col]
                            )

                # Rotate x-axis labels
                plt.xticks(rotation=90, fontsize=18)  # was ~8 → doubled
                plt.yticks(fontsize=18)

                # Labels and title with larger font
                plt.ylabel(col.replace("_", " "), fontsize=20)          # was ~9 → doubled
                #plt.title(f"{col.replace("_", " ")} After {season} Seasons", fontsize=22)  # was ~10 → doubled

                plt.grid(axis="y", linestyle="--", alpha=0.6)
                plt.tight_layout()
                plt.show()



        for team in teams:
            team.clear_season_stats()
            team.update_strength()



def experiment_50(field):


    NUM_RUNS = 50
    SEASONS_PER_RUN = 100
    NUM_TEAMS = 30

    # --------------------------------------------------
    # store strength history per team name
    # --------------------------------------------------
    team_history = defaultdict(list)
    # --------------------------------------------------
    # initialize ONCE
    # --------------------------------------------------
    base_teams = initialize_teams(NUM_TEAMS)

    for run in range(NUM_RUNS):

        print(f"Simulation {run + 1}/{NUM_RUNS}")

        # deep copy ensures identical starting state
        teams = copy.deepcopy(base_teams)

        for season in range(SEASONS_PER_RUN):

            
            spread_strength(teams)
            regular_season_simulate(teams)
            playoff_simulate(teams)

            lottery_index_after_season(teams)
            draft_simulate(teams)
            lottery_index_after_draft(teams)

            end_season(teams)

            for team in teams:
                team.clear_season_stats()
                team.update_strength()
        # collect final-season value
        for team in teams:
            team_history[team.name].append(
                getattr(team, field)
            )

    # -------------------------------
    # statistics
    # -------------------------------
    rows = []

    for team, values in team_history.items():
        rows.append({
            "team": team,
            "mean": np.mean(values),
            "min": np.min(values),
            "max": np.max(values),
            "std": np.std(values)
        })

    df = pd.DataFrame(rows)
    df.sort_values("mean", ascending=False, inplace=True)

    df.to_csv(f"results/{field}_statistics.csv", index=False)

    # -------------------------------
    # plot
    # -------------------------------
    x = np.arange(len(df))

    plt.figure(figsize=(18, 7))

    plt.bar(x, df["mean"], width=0.6, label="Mean")

    plt.fill_between(
        x,
        df["mean"] - df["std"],
        df["mean"] + df["std"],
        alpha=0.25,
        label="±1 Std Dev"
    )

    plt.plot(
        x,
        df["min"],
        linestyle="--",
        color="lightcoral",
        label="Min"
    )

    plt.plot(
        x,
        df["max"],
        linestyle="--",
        color="seagreen",
        label="Max"
    )

    # Font size adjustments
    plt.xticks(x, df["team"], rotation=90, fontsize=18)  # doubled from ~8
    plt.yticks(fontsize=18)
    plt.ylabel(field.replace("_", " "), fontsize=20)
   # plt.title(
    #f"{field} distribution after {SEASONS_PER_RUN} seasons\n"
    #f"({NUM_RUNS} independent simulations)",
    #fontsize=20
    #)
    plt.legend(fontsize=16)  # enlarge legend font

    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()



def graph_attribute_over_years(num_teams_to_plot, field):

    NUM_TEAMS = 30
    TOTAL_SEASONS = 100

    # -------------------------------
    # Initialize teams
    # -------------------------------
    teams = initialize_teams(NUM_TEAMS)

    # -------------------------------
    # Select random teams to plot
    # -------------------------------
    selected_teams = np.random.choice(teams, size=num_teams_to_plot, replace=False)

    # -------------------------------
    # Track the field over seasons
    # -------------------------------
    history = {team.name: [] for team in selected_teams}

    for season in range(TOTAL_SEASONS):
        spread_strength(teams)
        regular_season_simulate(teams)
        playoff_simulate(teams)
        lottery_index_after_season(teams)
        draft_simulate(teams)
        lottery_index_after_draft(teams)
        end_season(teams)

        for team in selected_teams:
            history[team.name].append(getattr(team, field))
        
        for team in teams:
            team.clear_season_stats()
            team.update_strength()

    # -------------------------------
    # Plot the attribute over seasons
    # -------------------------------
    plt.figure(figsize=(18, 7))
    
    for team_name, values in history.items():
        plt.plot(range(1, TOTAL_SEASONS + 1), values, marker='o', label=team_name)

    # Font size adjustments
    plt.xlabel("Season", fontsize=20)
    plt.ylabel(field.replace("_", " "), fontsize=20)
    #plt.title(
    #    f"{field} over {TOTAL_SEASONS} seasons for {num_teams_to_plot} random teams",
    #    fontsize=20
    #)
    plt.xticks(
        range(1, TOTAL_SEASONS + 1, max(1, TOTAL_SEASONS // 10)),
        fontsize=18
    )
    plt.yticks(fontsize=18)
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.legend(fontsize=16)
    plt.tight_layout()
    plt.show()


def playoff_index_gap(teams):
    """
    Compute the gap between:
    - the top 2 non-playoff teams (max pre-adjust lottery_index)
    - the bottom 2 playoff teams (min pre-adjust lottery_index)
    
    Returns the gap for the season.
    """
    # Split teams
    playoff_teams = [t for t in teams if t.playoff_rank >= 0]
    non_playoff_teams = [t for t in teams if t.playoff_rank == -1]


    # Sort by season wins
    playoff_sorted = sorted(playoff_teams, key=lambda x: x.season_wins)  # worst first
    non_playoff_sorted = sorted(non_playoff_teams, key=lambda x: x.season_wins, reverse=True)  # best first

    # Select the teams
    worst2_playoff = playoff_sorted[:2]
    best2_non_playoff = non_playoff_sorted[:2]

    # Pre-adjust lottery index (we can use `lottery_index` as is if captured before draft)
    min_pre_diminish = min(t.lottery_index for t in worst2_playoff)
    max_pre_increment = max(t.lottery_index for t in best2_non_playoff)

    # Compute gap
    gap = max_pre_increment - min_pre_diminish
    return gap


def edge_case_lottery_index(num_seasons=1000, num_teams=30):
    
    teams = initialize_teams(num_teams)
    total_indices_per_season_arr = []
    max_lottery_per_season = []
    gaps = []
    edge_case_impacts = []
    max_impc = 0

    for season in range(num_seasons):
        spread_strength(teams)
        regular_season_simulate(teams)
        playoff_simulate(teams)

        gap = playoff_index_gap(teams)
        if gap is not None:
            gaps.append(gap)

        # Calculate lottery index after season (before draft adjustments)
        lottery_index_after_season(teams)

        # Now sum lottery indices **only for lottery-eligible teams** (non-playoff)
        total_indices_arr = [t.lottery_index for t in teams if t.playoff_rank == -1]
        sum_indicies_per_season = sum(total_indices_arr)
        total_indices_per_season_arr.append(sum_indicies_per_season)


        # Track maximum lottery index among non-playoff teams
        max_indices_team = max(total_indices_arr)
        max_lottery_per_season.append(max_indices_team)

        impact = max_indices_team / (sum_indicies_per_season - gap) - max_indices_team / sum_indicies_per_season
        max_impc = max(impact, max_impc)
        edge_case_impacts.append(impact)


        # Continue with draft, update strength, etc.
        draft_simulate(teams)
        lottery_index_after_draft(teams)
        end_season(teams)

        for t in teams:
            t.clear_season_stats()
            t.update_strength()

    average_indices = np.mean(total_indices_per_season_arr)
    average_max_lottery = np.mean(max_lottery_per_season)
    avg_gap = np.mean(gaps)
    print(f"Average playoff index gap over {num_seasons} seasons: {avg_gap:.3f}")
    print(f"Average sum of lottery indices over {num_seasons} seasons: {average_indices:.3f}")
    print(f"Average maximum lottery index over {num_seasons} seasons: {average_max_lottery:.3f}")

    # Count how many impacts exceed 1.5% (0.015)
    over_1_5_percent = sum(1 for x in edge_case_impacts if x > 0.015)
    percent_over = over_1_5_percent / num_seasons * 100
    print(f"Out of {num_seasons} seasons, {over_1_5_percent} ({percent_over:.2f}%) have edge-case impacts over 1.5%")
    print(f"Largest edge-case impact on a team: {max(edge_case_impacts):.6f}")




if __name__ == "__main__":
    #graph1000(['avg_draft_pick', 'playoff_round_1'])
    experiment_50("max_playoff_streak")
    #graph_attribute_over_years(2, 'lottery_index')
    #edge_case_lottery_index()

from .simulation import initialize_teams, regular_season_simulate, playoff_simulate, tickets_after_season, tickets_after_draft, draft_simulate, end_season
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
    for season in range(num_seasons):
        print(f"Simulating season {season+1}/{num_seasons}")

        # Regular season and playoffs
        regular_season_simulate(teams)
        playoff_simulate(teams)

        # Update tickets and draft
        tickets_after_season(teams)
        draft_simulate(teams)
        tickets_after_draft(teams)

        # End season (updates totals and averages)
        end_season(teams)

        if season == num_seasons - 1: # save last season stats for a file
            df = pd.DataFrame([team.to_dict() for team in teams])
            df.to_csv(output_file, index=False)

        for team in teams:
            team.clear_season_stats()
            team.update_strength()

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

        plt.xticks(rotation=90)
        plt.ylabel(col)
        plt.title(f"{col} After {num_seasons} Seasons")

        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()



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

            regular_season_simulate(teams)
            playoff_simulate(teams)

            tickets_after_season(teams)
            draft_simulate(teams)
            tickets_after_draft(teams)

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

    plt.xticks(x, df["team"], rotation=90)
    plt.ylabel(field)
    plt.title(
        f"{field} distribution after {SEASONS_PER_RUN} seasons\n"
        f"({NUM_RUNS} independent simulations)"
    )

    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()








if __name__ == "__main__":
    #graph1000(['avg_season_wins', 'tickets'])
    experiment_50("avg_season_wins")
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

from constants import TEAM_NAME_MAP

TEAM_RANK_BASE_URL = 'https://www.basketball-reference.com/leagues/NBA'
DRAFT_PICK_BASE_URL = 'https://basketball.realgm.com/nba/draft/lottery_results/'


# Data for team rankings
def scrape_teams(start_year, end_year):

    # set up db
    columns = ['year', 'team', 'rank_regular', 'rank_playoffs']
    rows = []

    # get the general team data
    for year in range(start_year, end_year + 1):
        time.sleep(4)

        # finding all teams
        url = f'{TEAM_RANK_BASE_URL}_{year}_standings.html'
        response = requests.get(url)
        html = response.text
        html = html.replace('<!--', '').replace('-->', '')
        soup = BeautifulSoup(html, 'html.parser')

        # Table for teams conference
        table = soup.find('table', id='expanded_standings')
        for tr in table.find('tbody').find_all('tr'):
            rank_regular = tr.find('th', {'data-stat': 'ranker'}).get_text()
            team_name = tr.find('td', {'data-stat': 'team_name'}).get_text()
            team_name = ''.join(ch for ch in team_name if ch.isalpha() or ch.isspace() or ch.isdigit()).strip()
            rows.append([year, team_name, rank_regular, -1])

    # save initial data to df
    df = pd.DataFrame(rows, columns=columns)

    # find the ranks based on playoffs
    for year in range(start_year, end_year + 1):
        time.sleep(4)
        
        # Playoff info
        url = f'{TEAM_RANK_BASE_URL}_{year}.html'
        response = requests.get(url)
        html = response.text
        html = html.replace('<!--', '').replace('-->', '')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Table for playoffs
        playoff_rows = soup.find('table', id='all_playoffs').find_all('tr')
        for tr in playoff_rows:

            # extract data from tr
            tds = tr.find_all('td')

            # make sure we select rows with team names
            if not tds[0].find('span', class_='tooltip opener'):
                continue

            # get teams
            first_td_text = tds[0].get_text(strip=True)
            teams = tds[1].find_all('a')
            winner = teams[0].get_text(strip=True)
            loser = teams[1].get_text(strip=True)

            # add 1 to the winner team rank
            df.loc[(df['team'] == winner) & (df['year'] == year), 'rank_playoffs'] += 1
            # make sure we add 1 to both teams rank since they made it to playoff
            if 'First Round' in first_td_text:
                df.loc[((df['team'] == loser) | (df['team'] == winner)) & (df['year'] == year), 'rank_playoffs'] += 1
            
    # save df
    df.to_csv(f'data/TeamsRank_{start_year}-{end_year}.csv')
    return df


# Data for draft picks
def scrape_draft_picks(start_year, end_year):
    columns = ['year', 'pick', 'pick_team', 'player', 'draft_team', 'extra_check']
    rows = []

    for year in range(start_year, end_year + 1):

        # finding all teams
        url = f'{DRAFT_PICK_BASE_URL}{year}'
        response = requests.get(url)
        html = response.text
        html = html.replace('<!--', '').replace('-->', '')
        soup = BeautifulSoup(html, 'html.parser')

        # Table for draft picks
        table = soup.find('table')
        pick = 0
        for tr in table.find('tbody').find_all('tr'):
            pick += 1
            data = tr.find_all('td')
            # only for 1st 4 teams
            if pick > 4:
                break
            rows.append([year, 
                         data[0].get_text(strip=True), 
                         data[1].get_text(strip=True),
                         data[7].get_text(strip=True),
                         data[8].get_text(strip=True),
                         data[1].get_text(strip=True) != data[8].get_text(strip=True)])
            
    # save initial data to df
    df = pd.DataFrame(rows, columns=columns)

    # save df
    df.to_csv(f'data/DraftPicks_{start_year}-{end_year}.csv')
    return df


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
        return TEAM_NAME_MAP.get(lower_name, lower_name)
    return team_name # Return as is if not a string (e.g., NaN, None)


def normalize_data():
    # === Load Excel files ===

    playoff_df = pd.read_csv('data/TeamsRank_1985-2024.csv')
    playoff_df.columns = playoff_df.columns.str.strip()
    # Apply normalization to team names in playoff_df
    playoff_df['team_normalized'] = playoff_df['team'].apply(normalize_team_name)
    playoff_df['year'] = playoff_df['year'].astype(int)
    playoff_df.to_csv(f'data/TeamsRank_1985-2024.csv')

    draft_df = pd.read_csv('data/DraftPicks_1985-2024.csv')
    draft_df.columns = draft_df.columns.str.strip()
    # Apply normalization to team names in draft_df
    draft_df['pick_team_normalized'] = draft_df['pick_team'].apply(normalize_team_name)
    draft_df['year'] = draft_df['year'].astype(int)
    draft_df.to_csv(f'data/DraftPicks_1985-2024.csv')
    


def main():

    folder = 'data'
    if not os.path.exists(folder):
        os.makedirs(folder)
    #scrape_teams(1985, 2024)
    #scrape_draft_picks(1985, 2024)
    normalize_data()


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


TEAM_RANK_BASE_URL = 'https://www.basketball-reference.com/leagues/NBA'


# Data for team rankings
def scrape_teams(start_year, end_year):

    # set up db
    columns = ['year', 'rank', 'team']
    rows = []

    for year in range(start_year, end_year + 1):

        url = f'{TEAM_RANK_BASE_URL}_{year}_standings.html'
        response = requests.get(url)
        html = response.text
        html = html.replace('<!--', '').replace('-->', '')
        soup = BeautifulSoup(html, 'html.parser')

        # Table for east conference
        table = soup.find('table', id='expanded_standings')
        for tr in table.find('tbody').find_all('tr'):
            rank = tr.find('th', {'data-stat': 'ranker'}).get_text()
            team_name = tr.find('td', {'data-stat': 'team_name'}).get_text()
            team_name = ''.join(ch for ch in team_name if ch.isalpha() or ch.isspace()).strip()
            rows.append([year, rank, team_name])


    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(f'data/TeamsRank_{start_year}-{end_year}.csv')
    return df


# table for the payoff final teams
def scrape_playoff(start_year, end_year):

    # set up db
    columns = ['year', 'place', 'team']
    rows = []

    for year in range(start_year, end_year + 1):

        url = f'{TEAM_RANK_BASE_URL}_{year}.html'
        response = requests.get(url)
        html = response.text
        html = html.replace('<!--', '').replace('-->', '')
        soup = BeautifulSoup(html, 'html.parser')

        # find final teams row
        table_playoff = soup.find('table', id='all_playoffs')
        finals_row = table_playoff.find("tr")
        teams = finals_row.find_all("a", href=True)

        # Extract the team names
        team1 = teams[0].text.strip()
        rows.append([year, 1, team1])
        team2 = teams[1].text.strip()
        rows.append([year, 2, team2])

    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(f'data/PlayOff_{start_year}-{end_year}.csv')
    return df






from docx import Document

def main():

    folder = 'data'
    if not os.path.exists(folder):
        os.makedirs(folder)
    scrape_teams(2023, 2025)
    scrape_playoff(2023, 2025)


if __name__ == "__main__":
    main()

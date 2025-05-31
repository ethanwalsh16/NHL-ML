import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_leafs_games(season=2024):
    """
    Scrapes Toronto Maple Leafs game data for a given NHL season from hockey-reference.com.
    Skips the over-header and any interspersed header rows.
    Returns a cleaned DataFrame with the results.
    """
    from bs4 import Comment
    url = f"https://www.hockey-reference.com/teams/TOR/{season}_gamelog.html"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table, even if it's inside a comment
    table = soup.find('table', {'id': 'team_games'})
    if table is None:
        raise ValueError("Could not find games table on the page.")

    df = pd.read_html(str(table))[0]
    df = df[df['Score'] != 'Score'].reset_index(drop=True)
    return df

if __name__ == "__main__":
    # Example usage: scrape 2024 season and save to CSV
    df = scrape_leafs_games(2023)
    df.to_csv("leafs_data_scraped.csv", index=False)
    print("Scraped data saved to leafs_data_scraped.csv")

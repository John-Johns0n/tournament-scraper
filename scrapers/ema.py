import requests
from bs4 import BeautifulSoup

from scrapers import sanitization


def ema_scraper(tournament_code: str, event_id: str) -> list[list]:
    """
    Scrapes EMA tournament results from the internet.

    :param tournament_code: EMA tournament code (part of the url)
    :param event_id: Event ID for the database
    :return: Tournament results data
    """

    url = f'http://mahjong-europe.org/ranking/Tournament/{tournament_code}.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    results_table = soup.find('div', class_='TCTT_lignes')
    results_rows = results_table.find_all('div')
    results_rows.pop(0)  # Remove header

    tournament_results = [['event_id', 'player_id', 'first_name', 'last_name', 'placement', 'score']]

    for row in results_rows:
        cells = row.find_all('p')

        first_name = cells[3].text.capitalize().strip()
        last_name = cells[2].text.capitalize().strip()

        # Handle EMA guests
        if first_name == '- ema guest -':
            first_name = last_name.split(' ')[0]
            last_name = last_name.split(' ')[1].capitalize()

        # Handle unregistered players (full name is in first name field, last name field is '-')
        if last_name == '-':
            names = first_name.split(' ')
            first_name = names[0]
            last_name = ' '.join(names[1:])

        # Handle empty last names (NOT the same)
        if last_name == '':
            last_name = '(last name)'

        # Handle empty first names (why is this even allowed?
        if first_name == '-':
            first_name = '(first name)'

        # Handle capitalizing hyphenated/multiple names
        first_name, last_name = sanitization.capitalize_multiple_names(first_name, last_name)

        placement = cells[0].text.strip()
        score = cells[6].text.strip()

        data = [event_id, '', first_name, last_name, placement, score]
        tournament_results.append(data)

    return tournament_results

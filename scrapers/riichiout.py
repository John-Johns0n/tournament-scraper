import requests
from bs4 import BeautifulSoup

from scrapers import sanitization


def riichiout_scraper(tournament_code: str, event_id: str) -> list[list]:
    """
    Scrapes RiichiOut tournament results from the internet.

    :param tournament_code: RiichiOut tournament code (part of the url)
    :param event_id: Event ID for the database
    :return: Tournament results data
    """

    url = f'https://riichiout.com/tournaments/{tournament_code}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    results_table = soup.find('table', class_='rankings')
    rows = results_table.find_all('tr')

    tournament_results = [['event_id', 'player_id', 'first_name', 'last_name', 'placement', 'score']]

    for row in rows:
        cells = row.find_all('td')

        full_name = cells[1].find('a').text.strip()
        try:
            first_name, last_name = full_name.split(' ')
        except ValueError:  # No last name
            first_name = full_name
            last_name = '(last name)'

        first_name, last_name = sanitization.capitalize_multiple_names(first_name, last_name)

        placement = cells[0].text.strip('stndrth ')
        if placement == 'DNF':
            placement = 9999

        score = cells[2].text.split('/')[0].strip(' +')
        if score == 'DNF':
            score = None
        else:
            score = int(float(score.replace('−', '-')) * 1000)  # Replace Unicode minus with ASCII minus

        tournament_results.append([event_id, '', first_name, last_name, placement, score])

    return tournament_results

import requests
from bs4 import BeautifulSoup

from scrapers import sanitization


def wrc_scraper(tournament_code: str, event_id: str) -> list[list]:
    """
    Scrapes WRC tournament results from the internet.

    :param tournament_code: WRC edition (part of the url)
    :param event_id: Event ID for the database
    :return: Tournament results data
    """

    url = f'https://worldriichi.org/{tournament_code}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    first_name_tds = soup.find_all('td', class_='table-cell-3')
    last_name_tds = soup.find_all('td', class_='table-cell-2')
    placement_tds = soup.find_all('td', class_='table-cell-1')
    # country_tds = soup.find_all('td', class_='table-cell-4')

    wrc_results = [['event_id', 'player_id', 'first_name', 'last_name', 'placement', 'score']]

    for first_name_td, last_name_td, placement_td in zip(first_name_tds, last_name_tds, placement_tds):
        first_name = first_name_td.text.strip()
        last_name = last_name_td.text.strip(', ')
        if last_name in ('', '-'):
            last_name = '(last name)'

        first_name, last_name = sanitization.capitalize_multiple_names(first_name, last_name)

        placement = placement_td.text.strip()

        data = [event_id, '', first_name, last_name, placement, '']
        wrc_results.append(data)

    return wrc_results

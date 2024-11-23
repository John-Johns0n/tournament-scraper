import requests
from bs4 import BeautifulSoup


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

        first_name = cells[3].text.capitalize()
        last_name = cells[2].text.capitalize()
        if first_name == '- ema guest -':
            first_name = last_name.split(' ')[0]
            last_name = last_name.split(' ')[1].capitalize()

        placement = cells[0].text
        score = cells[6].text

        data = [event_id, '', first_name, last_name, placement, score]
        tournament_results.append(data)

    return tournament_results

import requests
from bs4 import BeautifulSoup


def wrc_scraper(tournament_code: str, event_id: str) -> list[list[str, str, int]]:
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
        first_name = first_name_td.text.capitalize()
        last_name = last_name_td.text.capitalize()
        placement = placement_td.text
        data = [event_id, '', first_name, last_name, placement, '']
        wrc_results.append(data)

    return wrc_results


def ema_scraper(tournament_code: str, event_id: str) -> list[list[str, str, int]]:
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


def riichiout_scraper(tournament_code: str, event_id: str) -> list[list[str, str, int]]:
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
        placement = cells[0].text.rstrip('stndrth')
        full_name = cells[1].find('a').text
        try:
            first_name, last_name = full_name.split(' ')
        except ValueError:  # No last name
            first_name = full_name
            last_name = '(last name)'
        score = cells[2].text.split('/')[0].strip(' +')

        tournament_results.append([event_id, '', first_name, last_name, placement, score])

    return tournament_results

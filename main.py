import requests
import csv
from bs4 import BeautifulSoup


def wrc_scraper(wrc_edition: str, event_id: str) -> list[list[str, str, int]]:
    """
    Scrapes WRC tournament results from the internet.

    :param wrc_edition: WRC edition (part of the url)
    :param event_id: Event ID for the database
    :return: Tournament results data
    """

    url = f'https://worldriichi.org/{wrc_edition}'
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


def write_to_csv(filename: str, data: list[list[str, str, int]]) -> None:
    """
    Writes a tournament's results to a CSV file.

    :param filename: Name to give the CSV file
    :param data: Results data
    """

    with open(f'{filename}.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


if __name__ == '__main__':
    wrc_2014 = wrc_scraper(wrc_edition='paris-2014', event_id='2014-010001')
    wrc_2017 = wrc_scraper(wrc_edition='las-vegas-2017', event_id='2017-010001')
    wrc_2022 = wrc_scraper(wrc_edition='vienna-2022', event_id='2022-010001')

    write_to_csv(filename='wrc_2014_results', data=wrc_2014)
    write_to_csv(filename='wrc_2017_results', data=wrc_2017)
    write_to_csv(filename='wrc_2022_results', data=wrc_2022)

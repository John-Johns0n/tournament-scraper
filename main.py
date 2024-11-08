import csv
from typing import Callable

from scrapers import wrc_scraper, ema_scraper, riichiout_scraper


def write_to_csv(filename: str, data: list[list[str, str, int]]) -> None:
    """
    Writes a tournament's results to a CSV file.

    :param filename: Name to give the CSV file
    :param data: Results data
    """

    with open(f'./results/{filename}.csv', mode='w', encoding='utf-8', newline='') as results_file:
        writer = csv.writer(results_file)
        writer.writerows(data)


def scrape_tournaments(path: str, scraper: Callable) -> None:
    """
    Scrapes the web for tournament results and outputs them to a CSV file.

    :param scraper: Scraper function to use (EMA, WRC, etc.)
    :param path: The path to the CSV file containing data for the tournaments to scrape
    """

    with open(path, mode='r', encoding='utf-8', newline='') as tournaments:
        csv_reader = csv.DictReader(tournaments, delimiter=',', quotechar='"')
        for row in csv_reader:
            print(f"Scraping results for {row['results_file_name'].removesuffix('_results')}")
            data = scraper(tournament_code=row['tournament_code'], event_id=row['event_id'])
            write_to_csv(filename=row['results_file_name'], data=data)
            print("Done! Moving to next tournament in queue.\n")


if __name__ == '__main__':
    scrape_tournaments(path='./tournaments/wrc.csv', scraper=wrc_scraper)
    scrape_tournaments(path='./tournaments/ema.csv', scraper=ema_scraper)

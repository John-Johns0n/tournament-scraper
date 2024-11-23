import csv
from typing import Callable

from scrapers import wrc, ema, riichiout


def write_to_csv(filename: str, path: str, data: list[list[str, str, int]]) -> None:
    """
    Writes a tournament's results to a CSV file.

    :param filename: Name to give the CSV file
    :param path: Destination path
    :param data: Results data
    """

    with open(f'{path}/{filename}.csv', mode='w', encoding='utf-8', newline='') as results_file:
        writer = csv.writer(results_file)
        writer.writerows(data)


def scrape_tournaments(data_path: str, destination_path: str, scraper: Callable) -> None:
    """
    Scrapes the web for tournament results and outputs them to a CSV file.

    :param data_path: The path to the CSV file containing data for the tournaments to scrape
    :param destination_path: Where to save the tournament results
    :param scraper: Scraper function to use (EMA, WRC, etc.)
    """

    with open(data_path, mode='r', encoding='utf-8', newline='') as tournaments:
        csv_reader = csv.DictReader(tournaments, delimiter=',', quotechar='"')
        for row in csv_reader:
            print(f"Scraping results for {row['results_file_name'].removesuffix('_results')}")
            data = scraper(tournament_code=row['tournament_code'], event_id=row['event_id'])
            write_to_csv(filename=row['results_file_name'], path=destination_path, data=data)
            print("Done! Moving to next tournament in queue.\n")


def main() -> None:
    scrape_tournaments(
        data_path='./tournaments/wrc.csv',
        destination_path='./results/wrc',
        scraper=wrc.wrc_scraper
    )
    scrape_tournaments(
        data_path='./tournaments/ema.csv',
        destination_path='./results/ema',
        scraper=ema.ema_scraper
    )
    scrape_tournaments(
        data_path='./tournaments/riichiout.csv',
        destination_path='results/riichiout',
        scraper=riichiout.riichiout_scraper
    )


if __name__ == '__main__':
    main()

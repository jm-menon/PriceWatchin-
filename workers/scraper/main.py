from scraper import scrape
from repository import clear_price_history_if_limit_exceeded
from prometheus_client import start_http_server
import os
import time


PRICE_HISTORY_MAX_RECORDS = int(os.getenv("PRICE_HISTORY_MAX_RECORDS", "200"))


def main():
    print("Starting metrics server...")
    start_http_server(8008)

    print("Starting scraper...")

    while True:
        scrape()
        clear_price_history_if_limit_exceeded(PRICE_HISTORY_MAX_RECORDS)
        time.sleep(30)

if __name__ == "__main__":
    main()

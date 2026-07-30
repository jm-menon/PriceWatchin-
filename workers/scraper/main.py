from scraper import scrape
from prometheus_client import start_http_server
import time


def main():
    print("Starting metrics server...")
    start_http_server(8008)

    print("Starting scraper...")

    while True:
        scrape()
        time.sleep(30)

if __name__ == "__main__":
    main()
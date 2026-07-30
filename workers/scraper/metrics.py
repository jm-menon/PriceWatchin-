from prometheus_client import Counter, Histogram

REQUEST_COUNT=Counter(
    "Scraper_request_count",
    "total number of scrapes made"
)

REQUEST_LATENCY=Histogram(
    "Scraper_latency_measure",
    "calculating amount of latency"
)
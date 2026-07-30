from prometheus_client import Counter, Histogram

#_total
REQUEST_COUNT=Counter(
    "Scraper_request_count",
    "total number of scrapes made"
)

#_count
REQUEST_LATENCY=Histogram(
    "Scraper_latency_measure",
    "calculating amount of latency"
)
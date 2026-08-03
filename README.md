# PriceWatchin-
I have 5 minulated ecommerce sights (check)
each of these + the scrapper i will run from docker (check)
scrapper will perform a health check before scrapping a particular sight (check)

add a history api end for each vendor
output the best price for a product-> or rather give result in a sorted manner
celery beat for scheduling the scrapper

## Price history retention

After every scraper cycle, the scraper checks the total row count in `price_history`.
When it exceeds `PRICE_HISTORY_MAX_RECORDS` (default: `200`), it clears the table and
invalidates cached price-search responses. Set `PRICE_HISTORY_MAX_RECORDS` in `.env` to
change the threshold.

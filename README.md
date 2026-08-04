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

## Deploying to Render

This repository includes `render.yaml` for a Blueprint deployment. It creates the
public frontend, private tracker and vendor APIs, scraper worker, Render Postgres,
and Render Key Value. The tracker performs a one-time database schema and seed
initialization during its first deployment.

Private services and background workers require paid Render plans. Review the
Blueprint's selected plans before confirming deployment.

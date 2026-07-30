import requests
from metrics import REQUEST_COUNT, REQUEST_LATENCY
import time

def health_check(base_url):
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(response.status_code)
        return response.status_code == 200
    except requests.RequestException:
        return False
    
def fetch_product(base_url, product_id, vendor_id):
    url = f"{base_url}/products-site-{vendor_id}/{product_id}"
    print(f"Fetching product from URL: {url}")
    start = time.perf_counter()
    REQUEST_COUNT.inc()
    print(REQUEST_COUNT.inc())
    response = requests.get(
        url,
        timeout=5
    )
    print(response)
    response.raise_for_status()
    REQUEST_LATENCY.observe(time.perf_counter() - start)

    return response.json()

def fetch_history(vendor_id, product_id, base_url):
    url = f"{base_url}/history/{vendor_id}/{product_id}"
    print(f"Fetching history from URL: {url}")
    start = time.perf_counter()
    REQUEST_COUNT.inc()
    response = requests.get(
        url,
        timeout=5
    )
    print(response)
    response.raise_for_status()
    REQUEST_LATENCY.observe(time.perf_counter() - start)

    return response.json()
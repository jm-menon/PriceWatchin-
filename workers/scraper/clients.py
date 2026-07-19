import requests

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
    response = requests.get(
        url,
        timeout=5
    )
    print(response)
    response.raise_for_status()

    return response.json()

def fetch_history(vendor_id, product_id):
    url = f"http://localhost:8006/history/{vendor_id}/{product_id}"
    print(f"Fetching history from URL: {url}")
    response = requests.get(
        url,
        timeout=5
    )
    print(response)
    response.raise_for_status()

    return response.json()
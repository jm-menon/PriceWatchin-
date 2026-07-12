import requests

def health_check(base_url):
    url= f"{base_url}/health"
    try:
        response= requests.get(url, timeout=5)
        if response.raise_for_status():
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Health check failed for {base_url} with this exception: {e}")
        print("Vendor Skipped")
        return False
    
def fetch_product(base_url, product_id, vendor_id):

    url = f"{base_url}/products-site-{vendor_id}/{product_id}"

    response = requests.get(
        url,
        timeout=5
    )

    response.raise_for_status()

    return response.json()
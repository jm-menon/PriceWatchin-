import requests


def fetch_product(base_url, product_id, vendor_id):

    url = f"{base_url}/products-site-{vendor_id}/{product_id}"

    response = requests.get(
        url,
        timeout=5
    )

    response.raise_for_status()

    return response.json()
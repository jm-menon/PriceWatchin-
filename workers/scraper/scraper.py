from clients import fetch_products
from repository import get_all_products, get_all_vendors, write_price
from normalizers import normalize_data

def scrape():
    products= get_all_products()
    vendors= get_all_vendors()

    for vendor in vendors:
        vendor_id= vendor.vendor_id
        base_url= vendor.base_url

        for product in products:
            product_id= product.product_id
            try:
                data= fetch_products(base_url, product_id)
                normalized_data= normalize_data(data, vendor_id)
                product_id= normalized_data.product_id
                vendor_id= normalized_data.vendor_id
                price= normalize_data.price
                write_price(product_id, vendor_id, price)
            except Exception as e:
                print(f"Error scraping product {product_id} from vendor {vendor_id}: {e}")
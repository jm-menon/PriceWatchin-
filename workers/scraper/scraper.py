from clients import fetch_product, health_check
from repository import get_all_products, get_all_vendors, write_price
from normalizers import normalize_data

def scrape():
    products= get_all_products()
    vendors= get_all_vendors()
    if not vendors:
        print("No vendors found.")
        return
    for vendor in vendors:
        vendor_id= vendor.vendor_id
        base_url= vendor.base_url

        if not products:
            print(f"No products found for vendor {vendor_id}.")
            continue

        if(health_check(base_url)==False):
                    print(f"Health check failed for vendor {vendor_id}. Skipping products from this vendor.")
                    continue

        for product in products:
            product_id= product.product_id
            try:
                data= fetch_product(base_url, product_id, vendor_id)
                #print(1)
                normalized_data= normalize_data(data, vendor_id)
                #print(2)
                product_id= normalized_data.product_id
                #print(product_id)
                vendor_id= normalized_data.vendor_id
                #print(vendor_id)
                price= normalized_data.price
                #print(price, " done")
                write_price(product_id, vendor_id, price)
                print(f"Scraped product {product_id} from vendor {vendor_id} with price {price}.")
            except Exception as e:
                print(f"Error scraping product {product_id} from vendor {vendor_id}: {e}")
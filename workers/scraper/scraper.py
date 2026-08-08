from clients import health_check
from repository import (
    get_all_products,
    get_all_vendors,
    write_price,
)
from normalizers import normalize_data

from pqc_client import (
    perform_pqc_handshake,
    fetch_encrypted_price,
)


def scrape():

    products = get_all_products()
    vendors = get_all_vendors()

    if not vendors:
        print("No vendors found.")
        return

    for vendor in vendors:

        vendor_id = vendor.vendor_id
        base_url = vendor.base_url

        if not products:
            print(
                f"No products found for vendor {vendor_id}."
            )
            continue

        # ------------------------------------------------
        # 1. Check vendor health
        # ------------------------------------------------

        if not health_check(base_url):

            print(
                f"Health check failed for vendor "
                f"{vendor_id}. Skipping."
            )

            continue

        # ------------------------------------------------
        # 2. Establish hybrid PQC session
        # ------------------------------------------------

        try:

            print(
                f"Establishing PQC session "
                f"with vendor {vendor_id}..."
            )

            session = perform_pqc_handshake(
                base_url
            )

            print(
                f"PQC session established with "
                f"vendor {vendor_id}"
            )

        except Exception as e:

            print(
                f"PQC handshake failed for "
                f"vendor {vendor_id}: {e}"
            )

            continue

        # ------------------------------------------------
        # 3. Fetch every product through PQC session
        # ------------------------------------------------

        for product in products:

            product_id = product.product_id

            try:

                data = fetch_encrypted_price(
                    base_url,
                    session["session_id"],
                    session["session_key"],
                    product_id,
                )

                # ------------------------------------------------
                # 4. Existing normalization pipeline
                # ------------------------------------------------

                normalized_data = normalize_data(
                    data,
                    vendor_id,
                )

                # ------------------------------------------------
                # 5. Existing database pipeline
                # ------------------------------------------------

                write_price(
                    normalized_data.product_id,
                    normalized_data.vendor_id,
                    normalized_data.price,
                )

                print(
                    f"Scraped product "
                    f"{normalized_data.product_id} "
                    f"from vendor "
                    f"{normalized_data.vendor_id} "
                    f"with price "
                    f"{normalized_data.price}."
                )

            except Exception as e:

                print(
                    f"Error scraping product "
                    f"{product_id} from vendor "
                    f"{vendor_id}: {e}"
                )
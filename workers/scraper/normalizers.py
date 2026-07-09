from models import ScrapedPrice


#i could potentially normalize the data separately for each simulator depending on the ds of each simulator, but for now i will just normalize the data in a single function
def normalize_data(data: dict, vendor_id_data):
    if data.size()==0:
        return None
    for x in data:
        product_id= x["product_id"]
        price= x["price"]
        vendor_id= vendor_id_data
        scraped_price= ScrapedPrice(product_id= product_id, vendor_id= vendor_id, price= price)
        return scraped_price
import json
from sqlalchemy import text, engine
import os
from dotenv import load_dotenv

load_dotenv()
query= os.getenv("query_seed_products")

with open("shared/products.json") as f:
    products = json.load(f)

with engine.begin() as conn:
    for product in products:
        conn.excute(
            text(query), {
                "product_name": product["product_name"],
                "category": product["category"],
                "base_price": product["base_price"]
            }
        )
print("Products seeded successfully.")
import json
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set!")

engine = create_engine(DATABASE_URL, echo=True)   # echo=True helps debugging

query = os.getenv("query_seed_products")
if not query:
    raise ValueError("query_seed_products not found in .env")

with open("../shared/products.json", encoding="utf-8") as f:
    products = json.load(f)

print(f"Loaded {len(products)} products from JSON.")

inserted = 0

with engine.begin() as conn:        # This should auto-commit at the end
    # Check count before
    before = conn.execute(text("SELECT COUNT(*) FROM products")).scalar()
    print(f"Before insert: {before} products")

    for product in products:
        try:
            result = conn.execute(
                text(query),
                {
                    "product_name": product["product_name"],
                    "category": product.get("category"),
                    "base_price": product["base_price"]
                }
            )
            inserted += result.rowcount
            print(f"✅ Inserted: {product['product_name']}")
        except Exception as e:
            if "duplicate key" in str(e).lower():
                print(f"⏭️ Skipped (already exists): {product['product_name']}")
            else:
                print(f"❌ Error: {product['product_name']} → {e}")

    # Final count after inserts
    after = conn.execute(text("SELECT COUNT(*) FROM products")).scalar()
    print(f"After insert: {after} products")

print(f"\n🎉 Seeding finished. Rows affected: {inserted}")
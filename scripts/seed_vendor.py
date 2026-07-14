import json
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

VENDORS_FILE = BASE_DIR / "shared" / "vendor_prod.json"

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set!")

engine = create_engine(DATABASE_URL, echo=True)   # echo=True helps debugging

query = os.getenv("query_seed_vendor")
if not query:
    raise ValueError("query_seed_vendor not found in .env")

with open(VENDORS_FILE, encoding="utf-8") as f:   # Adjust path if needed
    vendors = json.load(f)

print(f"Loaded {len(vendors)} vendors from JSON.")

inserted = 0

with engine.begin() as conn:        # This should auto-commit at the end
    # Check count before
    before = conn.execute(text("SELECT COUNT(*) FROM vendor")).scalar()
    print(f"Before insert: {before} vendors")

    for v in vendors:
        try:
            result = conn.execute(
                text(query),
                {
                    "vendor_name": v["vendor_name"],
                    "base_url": v["base_url"]
                }
            )
            inserted += result.rowcount
            print(f"✅ Inserted: {v['vendor_name']}")
        except Exception as e:
            if "duplicate key" in str(e).lower():
                print(f"⏭️ Skipped (already exists): {v['vendor_name']}")
            else:
                print(f"❌ Error: {v['vendor_name']} → {e}")

    # Final count after inserts
    after = conn.execute(text("SELECT COUNT(*) FROM vendor")).scalar()
    print(f"After insert: {after} vendors")

print(f"\n🎉 Vendor seeding finished. Rows affected: {inserted}")
import os
from dotenv import load_dotenv
import json
from sqlalchemy import text, engine

load_dotenv()
query= os.getenv("query_seed_vendor")

with open("shared/vendor.json") as f:
    vendor= json.load(f)
    
with engine.begin() as conn:
    for v in vendor:
        conn.execute(
            text(query),{
                "vendor_name": v["vendor_name"],
                "base_url": v["base_url"]
            }
        )

print("Vendor seeded successfully.")

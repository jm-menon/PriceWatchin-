"""Create the schema and seed data for a new managed Postgres instance."""

import json
import os
from pathlib import Path

from sqlalchemy import create_engine, text


APP_DIR = Path(__file__).resolve().parent
DATABASE_URL = os.environ["DATABASE_URL"]


def execute_schema(connection):
    schema = (APP_DIR / "init.sql").read_text(encoding="utf-8")
    for statement in schema.split(";"):
        if statement.strip():
            connection.execute(text(statement))


def vendor_data():
    vendors = json.loads((APP_DIR / "shared" / "vendor_prod.json").read_text(encoding="utf-8"))
    for index, vendor in enumerate(vendors, start=1):
        hostport = os.getenv(f"SITE{index}_HOSTPORT")
        if hostport:
            vendor["base_url"] = f"http://{hostport}"
    return vendors


def main():
    engine = create_engine(DATABASE_URL)
    products = json.loads((APP_DIR / "shared" / "products.json").read_text(encoding="utf-8"))

    with engine.begin() as connection:
        execute_schema(connection)
        for product in products:
            connection.execute(
                text("""INSERT INTO products (product_name, category, base_price)
                VALUES (:product_name, :category, :base_price)
                ON CONFLICT (product_name) DO NOTHING"""),
                product,
            )
        for vendor in vendor_data():
            connection.execute(
                text("""INSERT INTO vendor (vendor_name, base_url)
                VALUES (:vendor_name, :base_url)
                ON CONFLICT (vendor_name) DO UPDATE SET base_url = EXCLUDED.base_url"""),
                vendor,
            )

    print("Database schema and seed data are ready.")


if __name__ == "__main__":
    main()

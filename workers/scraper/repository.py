from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
import dotenv
from cache import redis_client

env= dotenv.load_dotenv()
DATABASE_URL= os.getenv("DATABASE_URL")

engine= create_engine(DATABASE_URL)
Session= sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_all_products():
    session= Session()
    try:
        rows= session.execute(text("select product_id, product_name from products"))
        return rows.fetchall()
    except Exception as e:
        print(f"Error fetching products: {e}")

def get_all_vendors():
    session=Session()
    try:
        rows= session.execute(text("select vendor_id, vendor_name, base_url from vendor"))
        return rows.fetchall()
    except Exception as e:
        print(f"Error fetching vendors: {e}")

def write_price(product_id, vendor_id, price):
    session=Session()
    try:
        session.execute(text("insert into price_history (product_id, vendor_id, price) values (:product_id, :vendor_id, :price)"),{
            "product_id": product_id,
            "vendor_id": vendor_id,
            "price": price
        })
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error writing price: {e}")
        
    try:
        redis_client.delete(f"cheapest:{product_id}")
        redis_client.delete(f"history:{product_id}")
        redis_client.delete(f"vendor_history:{product_id}:{vendor_id}")
    except Exception as e:
        print(f"Redis failed with error: {e}")

def history_vendor_product(vendor_id, product_id):
    session= Session()
    try:
        rows= session.execute(text("select price from price_history where vendor_id= :vendor_id and product_id= :product_id order by created at desc"),{
            "vendor_id": vendor_id,
            "product_id": product_id
        })
        return rows.fetchall()
    except Exception as e:
        print(f"Error fetching vendor history: {e}")

def best_buy(product_id):
    session= Session()
    try:
        rows= session.execute(text("select vendor_id, price, product_id from price_history where product_id= :product_id and price=(select min(price) from price_history where product_id= :product_id)"),{
            "product_id": product_id
        })
        return rows.fetchall()
    except Exception as e:
        print(f"Error fetching best buy: {e}")
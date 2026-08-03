from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import get_db
import os
import dotenv
from sqlalchemy.orm import Session
from fastapi import Depends

env= dotenv.load_dotenv()
DATABASE_URL= os.getenv("DATABASE_URL")

engine= create_engine(DATABASE_URL)
Session= sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_price_history(product_id, date_from, date_to, db: Session= Depends(get_db)):
    result= db.execute(text("SELECT * FROM price_history WHERE product_id = :product_id AND " \
    "created_at::date BETWEEN :date_from AND :date_to"), 
    {"product_id": product_id, "date_from": date_from, "date_to": date_to})
    return result.fetchall()

def get_cheapest_product(product_id, date_from, date_to, db: Session= Depends(get_db)):
    result= db.execute(text("SELECT price, vendor_id FROM price_history WHERE product_id = :product_id AND " \
    "created_at::date BETWEEN :date_from AND :date_to ORDER BY price ASC LIMIT 1"), 
    {"product_id": product_id, "date_from": date_from, "date_to": date_to})
    return result.fetchone()

def get_product_vendor_history(product_id, vendor_id, date_from, date_to, db: Session= Depends(get_db)):
    result= db.execute(text("SELECT * FROM price_history WHERE product_id = :product_id AND " \
    "vendor_id = :vendor_id AND created_at::date BETWEEN :date_from AND :date_to ORDER BY created_at DESC"), 
    {"product_id": product_id, "vendor_id": vendor_id, "date_from": date_from, "date_to": date_to})
    return result.fetchall()
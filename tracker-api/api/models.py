from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__='products'
    product_id= Column(Integer, primary_key=True)
    product_name=Column(String(200), nullable=False)
    category=Column(String(200), nullable=False)


class Vendor(Base):
    __tablename__='vendor'
    vendor_id= Column(Integer, primary_key=True)
    vendor_name=Column(String(200), nullable=False)
    base_url=Column(String(200), nullable=False)

class Pricehistory(Base):
    __tablename__='pricehistory'
    price_id= Column(Integer, primary_key=True)
    product_id=Column(Integer, nullable=False)
    vendor_id=Column(Integer, nullable=False)
    price=Column(Float, nullable=False)
    created_at=Column(String(200), nullable=False)


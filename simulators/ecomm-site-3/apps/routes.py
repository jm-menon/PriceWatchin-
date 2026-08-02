from fastapi import APIRouter, HTTPException, Depends
from .models import Product
from typing import List
from sqlalchemy.orm import Session
from .database import get_db, get_all_items, get_item_id
import random

router= APIRouter()

@router.get("/", response_model=List[Product])
async def get_products(db: Session=Depends(get_db)):
    try:
        products= get_all_items(db)
        for p in products:
            p= dict(p)
            p["base_price"]=p["base_price"]
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error: Failure to retrieve data")


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session=Depends(get_db)):
    try:
        product= get_item_id(product_id, db)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found!")
        product= dict(product)
        product["base_price"]=product["base_price"]
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve product")
    ######
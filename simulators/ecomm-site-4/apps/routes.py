from fastapi import APIRouter, HTTPException, Depends
from .models import Product
from typing import List
from sqlalchemy.orm import Session
from .database import get_db, get_all_items, get_item_id
import random
import asyncio

router= APIRouter()

failure_chance= random.random()  # Generate a random float between 0.0 and 1.0

@router.get("/", response_model=List[Product])
async def get_products(db: Session=Depends(get_db)):
    if failure_chance<0.15:
        await asyncio.sleep(2)
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve products")
    try:
        products= get_all_items(db)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error: Failure to retrieve data")

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session=Depends(get_db)):
    if failure_chance<0.1:
        await asyncio.sleep(2)
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve products")
    await asyncio.sleep(
        random.uniform(0.5, 2.0)
    )
    try:
        product= get_item_id(product_id, db)
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve product")
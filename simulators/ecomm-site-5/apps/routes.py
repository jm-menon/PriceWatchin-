from fastapi import APIRouter, HTTPException, Depends
from .models import Product
from typing import List
from sqlalchemy.orm import Session
from .database import get_db, get_all_items, get_item_id
from collections import deque
import time
router= APIRouter()

@router.get("/", response_model=List[Product])
async def get_products(db: Session=Depends(get_db)):
    requests_get_all = deque()
    current = time.time()
    while requests_get_all and current - requests_get_all[0] > 60:
        requests_get_all.popleft()
    if len(requests_get_all) >= 100:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
    requests_get_all.append(current)
    try:
        products= get_all_items(db)
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error: Failure to retrieve data")


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session=Depends(get_db)):
    requests_get_one = deque()
    current = time.time()
    while requests_get_one and current - requests_get_one[0] > 60:
        requests_get_one.popleft()
    if len(requests_get_one) >= 100:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded"
        )
    requests_get_one.append(current)
    try:
        product= get_item_id(product_id, db)
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve product")
from fastapi import APIRouter, HTTPException, requests
from .models import Product
from typing import List
import json
import os
from collections import deque
import time
router= APIRouter()

def load_products_get()-> List[dict]:
    
    try:
        base_path= os.path.dirname(os.path.abspath(__file__))
        file_path= os.path.join(base_path, "products.json")
        
        with open(file_path, "r") as file:
            products= json.load(file)
            if isinstance(products, List): #standard expection is list, just gonna add dictionary with "product" for the sake of making it robust
                return products
            elif isinstance(products, dict) and "product" in products:
                return products["products"]
            else:
                return []   
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Products file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Server error: Failed to decode products file")
    
    return []

PRODUCT_RESULT= load_products_get()

@router.get("/", response_model=List[Product])
async def get_products():
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
    return PRODUCT_RESULT


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
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
        product= next((p for p in PRODUCT_RESULT if p["id"]==product_id), None)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found!")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve product")
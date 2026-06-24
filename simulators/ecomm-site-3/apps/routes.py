from fastapi import APIRouter, HTTPException
from .models import Product
from typing import List
import json
import os
import random

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
    for p in PRODUCT_RESULT:
        p["price"]= random.randint(-500, 500)+p["price"]
    return PRODUCT_RESULT

@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    try:
        product = next(
            (
                {
                    **p,
                    "price": p["price"] + random.randint(-500, 500)
                }
                for p in PRODUCT_RESULT
                if p["id"] == product_id
            ),
            None
    )
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found!")
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve product")
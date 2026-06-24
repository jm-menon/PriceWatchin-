from fastapi import APIRouter, HTTPException
from .models import Product
from typing import List
import json
import os

router= APIRouter()

def load_products_get()-> List[dict]:
    
    try:
        base_path= os.path.dirname(os.path.abspath(__file__))
        file_path= os.path.join(base_path, "products.json")
        
        with open(file_path, "r") as file:
            products= json.load(file)
            if isinstance(products, List):
                return products
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
    return PRODUCT_RESULT
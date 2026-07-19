from fastapi import APIRouter, HTTPException, Depends
from .models import PriceHistoryResponse, CheapestProductResponse
from typing import List
from sqlalchemy.orm import Session
from .repository import get_price_history, get_cheapest_product, get_product_vendor_history
from .database import get_db

router= APIRouter()


@router.get("/price_history/{product_id}", response_model=List[PriceHistoryResponse])
async def get_price_history_api(product_id: int, db: Session=Depends(get_db)):
    try:
        price_history= get_price_history(product_id, db)
        return price_history
    except Exception as e:
        print(f"Error occurred while fetching price history: {e}")
        raise HTTPException(status_code=500, detail="Server error: Failure to retrieve data")


@router.get("/cheapest_product/{product_id}", response_model=CheapestProductResponse)
async def get_cheapest_product_api(product_id: int, db: Session=Depends(get_db)):
    try:
        cheapest_product= get_cheapest_product(product_id, db)
        return cheapest_product
    except Exception as e:
        print(f"Error occurred while fetching cheapest product: {e}")
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve product")
    

@router.get("/product_vendor_history/{product_id}/{vendor_id}", response_model=PriceHistoryResponse)
async def get_product_vendor_history_api(product_id: int, vendor_id: int, db: Session=Depends(get_db)):
    try:
        product_vendor_history= get_product_vendor_history(product_id, vendor_id, db)
        return product_vendor_history
    except Exception as e:
        print(f"Error occurred while fetching product vendor history: {e}")
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve product vendor history")
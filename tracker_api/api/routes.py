import json
from fastapi import APIRouter, HTTPException, Depends
from models import PriceHistoryResponse, CheapestProductResponse
from typing import List
from sqlalchemy.orm import Session
from repository import get_price_history, get_cheapest_product, get_product_vendor_history
from database import get_db
from cache import redis_client
from metrics import REQUEST_COUNT, REQUEST_LATENCY, CACHE_HITS, CACHE_MISSES
import time

router= APIRouter()


@router.get("/price_history/{product_id}/{date_from}/{date_to}", response_model=List[PriceHistoryResponse])
#@REQUEST_LATENCY.time()
async def get_price_history_api(product_id: int, date_from: str, date_to: str, db: Session=Depends(get_db)):
    REQUEST_COUNT.inc()
    start = time.perf_counter()
    try:
        key = f"price_history:{product_id}:{date_from}:{date_to}"
        cached = redis_client.get(key)
        if cached:
            CACHE_HITS.inc()
            return json.loads(cached)
        CACHE_MISSES.inc()
        price_history= get_price_history(product_id, date_from, date_to, db)
        row = price_history[0]
        response = [
        {
        "price_id": row.price_id,
        "product_id": row.product_id,
        "vendor_id": row.vendor_id,
        "price": row.price,
        "created_at": row.created_at.isoformat()
        }
        for row in price_history
    ]
        redis_client.setex(
                        key,
                        300,
                    json.dumps(response)
                    )
        return response
    except Exception as e:
        print(f"Error occurred while fetching price history: {e}")
        raise HTTPException(status_code=500, detail="Server error: Failure to retrieve data")
    finally:
        REQUEST_LATENCY.observe(time.perf_counter() - start)


@router.get("/cheapest_product/{product_id}/{date_from}/{date_to}", response_model=CheapestProductResponse)
#@REQUEST_LATENCY.time()
async def get_cheapest_product_api(product_id: int, date_from: str, date_to: str, db: Session=Depends(get_db)):
    REQUEST_COUNT.inc()
    start = time.perf_counter()
    try:
        key = f"cheapest:{product_id}:{date_from}:{date_to}"
        cached = redis_client.get(key)
        if cached:
            CACHE_HITS.inc()
            return json.loads(cached)
        CACHE_MISSES.inc()
        cheapest_product= get_cheapest_product(product_id,date_from,date_to, db)
        response={
            "price": cheapest_product.price,
            "vendor_id": cheapest_product.vendor_id
        }
        redis_client.setex(
                        key,
                        300,
                    json.dumps(response)
                    )
        return response
    except Exception as e:
        print(f"Error occurred while fetching cheapest product: {e}")
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve product")
    finally:
        REQUEST_LATENCY.observe(time.perf_counter() - start)

    

@router.get("/product_vendor_history/{product_id}/{vendor_id}/{date_from}/{date_to}", response_model=list[PriceHistoryResponse])
#@REQUEST_LATENCY.time()
async def get_product_vendor_history_api(product_id: int, vendor_id: int, date_from: str, date_to: str, db: Session=Depends(get_db)):
    REQUEST_COUNT.inc()
    start=time.perf_counter()
    try:
        key = f"product_vendor_history:{product_id}:{vendor_id}:{date_from}:{date_to}"
        cached = redis_client.get(key)
        if cached:
            CACHE_HITS.inc()
            return json.loads(cached)
        CACHE_MISSES.inc()
        product_vendor_history= get_product_vendor_history(product_id, vendor_id, date_from, date_to, db)
        response = [
        {
        "price_id": row.price_id,
        "product_id": row.product_id,
        "vendor_id": row.vendor_id,
        "price": row.price,
        "created_at": row.created_at.isoformat()
        }
        for row in product_vendor_history
    ]
        redis_client.setex(
                        key,
                        300,
                    json.dumps(response)
                    )
        return response
    except Exception as e:
        print(f"Error occurred while fetching product vendor history: {e}")
        raise HTTPException(status_code=500, detail="Server error: Failed to retrieve product vendor history")
    finally:
        REQUEST_LATENCY.observe(time.perf_counter() - start)
import json

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from .models import Product, EncryptedPriceRequest
from .database import get_db, get_all_items, get_item_id

from shared.pqc.crypto import (
    encrypt_payload,
    b64_encode,
)

from shared.pqc.session import SESSIONS


router = APIRouter()


@router.get("/", response_model=List[Product])
async def get_products(
    db: Session = Depends(get_db),
):
    try:
        products = get_all_items(db)
        return products

    except Exception as e:
        print(f"Error fetching products: {e}")
        raise HTTPException(
            status_code=500,
            detail="Server error: Failure to retrieve data",
        )


@router.get("/{product_id}", response_model=Product)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    try:
        product = get_item_id(product_id, db)

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        return product

    except HTTPException:
        raise

    except Exception as e:
        print(f"Error fetching product: {e}")
        raise HTTPException(
            status_code=500,
            detail="Server error: Failed to retrieve product",
        )


@router.post("/encrypted-price")
async def encrypted_price(
    request: EncryptedPriceRequest,
    db: Session = Depends(get_db),
):
    # -----------------------------------------------
    # 1. Find the PQC session
    # -----------------------------------------------

    session_key = SESSIONS.get(request.session_id)

    if session_key is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired session",
        )

    # -----------------------------------------------
    # 2. Get the product
    # -----------------------------------------------

    product = get_item_id(
        request.product_id,
        db,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    # -----------------------------------------------
    # 3. Build the price response
    # -----------------------------------------------

    price_data = {
        "product_id": product.product_id,
        "vendor_id": 1,
        "price": product.price,
    }

    # -----------------------------------------------
    # 4. Convert JSON → bytes
    # -----------------------------------------------

    plaintext = json.dumps(
        price_data
    ).encode("utf-8")

    # -----------------------------------------------
    # 5. Encrypt using AES-GCM
    # -----------------------------------------------

    ciphertext, nonce = encrypt_payload(
        plaintext,
        session_key,
    )

    # -----------------------------------------------
    # 6. Return encrypted response
    # -----------------------------------------------

    return {
        "algorithm": "AES-256-GCM",
        "nonce": b64_encode(nonce),
        "ciphertext": b64_encode(ciphertext),
    }


from pydantic import BaseModel
from datetime import datetime


class PriceHistoryResponse(BaseModel):
    price_id: int
    product_id: int
    vendor_id: int
    price: float
    created_at: datetime


class CheapestProductResponse(BaseModel):
    vendor_id: int
    price: float
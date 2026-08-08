from pydantic import BaseModel

class Product(BaseModel):
    product_id: int
    product_name: str
    base_price: float


class EncryptedPriceRequest(BaseModel):
    session_id: str
    product_id: int
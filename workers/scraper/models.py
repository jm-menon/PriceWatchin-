from dataclasses import dataclass

@dataclass
class ScrapedPrice :
    product_id: int
    vendor_id: int
    price: float
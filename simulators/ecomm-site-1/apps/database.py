import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

load_dotenv()
DATABASE_URL= os.getenv("DATABASE_URL")

engine= create_engine(DATABASE_URL, echo=True, future=True)

def get_db():
    db= Session(engine)
    try:
        yield db
    finally:
        db.close()

def get_all_items(db: Session) -> List[dict]:
    try:
        statement= select(text("product_id"), 
                          text("product_name"), 
                          text("base_price")).select_from(text("products")).order_by(text("product_id"))
        result=db.execute(statement)
        return [dict(row._mapping) for row in result]
    except SQLAlchemyError as e:
        print(f"Error occurred while fetching items: {e}")
        return []

def get_item_id(item_id: int, db: Session) -> Optional[dict]:
    try:
        statement = (
            select(text("product_id"), text("product_name"), text("base_price"))
            .select_from(text("products"))
            .where(text("product_id = :pid").params(pid=item_id))
        )
        result = db.execute(statement)
        row = result.mappings().first()  # gets one row as a dict-like object, or None
        if row is None:
            return None
        return dict(row)
    except SQLAlchemyError as e:
        print(f"Error occurred while fetching item: {e}")
        return None
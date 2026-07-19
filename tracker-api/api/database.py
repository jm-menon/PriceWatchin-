#connecting to the database
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

load_dotenv()
DATABASE_URL= os.getenv("DATABASE_URL")

engine= create_engine(DATABASE_URL, echo=True, future=True)

def get_db():
    db= Session(engine)
    try:
        yield db
    finally:
        db.close()

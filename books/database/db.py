from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database.connection import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDependency = Annotated[Session, Depends(get_db)]
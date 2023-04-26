from fastapi import FastAPI, Depends, Path, HTTPException
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from pydantic import BaseModel, Field
from models import Book
import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

dbDependency = Annotated[Session, Depends(get_db)]


class BookIn(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    category: str = Field(min_length=3)
    rating: int  = Field(ge=1, le=5)


@app.get("/books", status_code=status.HTTP_200_OK)
async def getAllBooks(db: dbDependency):
    return db.query(Book).all()

@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def getOneBook(db: dbDependency, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).first()
    if book is not None:
        return book
    raise HTTPException(status_code=404, detail="Book not found!")

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def createBook(db: dbDependency, bookIn: BookIn):
    newBook = Book(**bookIn.dict())
    db.add(newBook)
    db.commit()

@app.put("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateBook(db: dbDependency, bookIn: BookIn, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found!")
    
    book.title = bookIn.title
    book.author = bookIn.author
    book.category = bookIn.category
    book.rating = bookIn.rating

    db.add(book)
    db.commit()

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def readBook(db: dbDependency, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found!")
    
    db.query(Book).filter(Book.id == id).delete()
    db.commit()
    
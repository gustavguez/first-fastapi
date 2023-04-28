from fastapi import APIRouter, Path, HTTPException
from starlette import status
from tablemodels.book import Book
from database.db import dbDependency
from pydantic import BaseModel, Field

router = APIRouter()

class BookIn(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    category: str = Field(min_length=3)
    rating: int  = Field(ge=1, le=5)

@router.get("/books", status_code=status.HTTP_200_OK)
async def getAllBooks(db: dbDependency):
    return db.query(Book).all()

@router.get("/books/{id}", status_code=status.HTTP_200_OK)
async def getOneBook(db: dbDependency, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).first()
    if book is not None:
        return book
    raise HTTPException(status_code=404, detail="Book not found!")

@router.post("/books", status_code=status.HTTP_201_CREATED)
async def createBook(db: dbDependency, bookIn: BookIn):
    newBook = Book(**bookIn.dict())
    db.add(newBook)
    db.commit()

@router.put("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def readBook(db: dbDependency, id: int = Path(gt=0)):
    book = db.query(Book).filter(Book.id == id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found!")
    
    db.query(Book).filter(Book.id == id).delete()
    db.commit()
    
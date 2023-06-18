from fastapi import APIRouter, Path, HTTPException
from starlette import status
from tablemodels.book import Book
from dependencies.db import dbDependency
from dependencies.oauth import oauth2Dependency
from pydantic import BaseModel, Field

router = APIRouter(
    tags=['books']
)


class BookIn(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    category: str = Field(min_length=3)
    rating: int = Field(ge=1, le=5)


@router.get("/books", status_code=status.HTTP_200_OK)
async def getAllBooks(user: oauth2Dependency, db: dbDependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated!")
    return db.query(Book).all()


@router.get("/books/{id}", status_code=status.HTTP_200_OK)
async def getOneBook(user: oauth2Dependency, db: dbDependency, id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated!")

    book = db.query(Book).filter(Book.id == id).first()
    if book is not None:
        return book
    raise HTTPException(status_code=404, detail="Book not found!")


@router.post("/books", status_code=status.HTTP_201_CREATED)
async def createBook(user: oauth2Dependency, db: dbDependency, bookIn: BookIn):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated!")
    print(user)
    newBook = Book(**bookIn.dict(), userId=user.get('id'))
    db.add(newBook)
    db.commit()


@router.put("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def updateBook(user: oauth2Dependency, db: dbDependency, bookIn: BookIn, id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated!")

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
async def readBook(user: oauth2Dependency, db: dbDependency, id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated!")

    book = db.query(Book).filter(Book.id == id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found!")

    db.query(Book).filter(Book.id == id).delete()
    db.commit()

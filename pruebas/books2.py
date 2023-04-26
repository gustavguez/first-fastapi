from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    category: str
    rating: int

    def __init__(self, id, title, author, category, rating):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.rating = rating

class BookIn(BaseModel):
    id: Optional[int]
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    category: str = Field(min_length=3)
    rating: int  = Field(ge=1, le=5)

books = [
    Book(1,  "El señor de los anillos 1", "R. Matt 1", "ficcion", 5),
    Book(2,  "El señor de los anillos 2", "R. Matt 1", "ficcion", 4),
    Book(3,  "It", "Melinda E", "terror", 4),
    Book(4,  "Finanzas Ninjas", "Carlos 3", "finanzas", 1)
]

def getNextBookId():
    return books[-1].id + 1

@app.get("/books")
async def readAllBooks(category: str = ''):
    result = books
    if(category):
        result = []
        for book in books:
            if(book.get("category").lower() == category.lower()):
                result.append(book)
    return result

@app.get("/books/{id}")
async def readBook(id: int = Path(gt=0)):
    for book in books:
        if(book.id == id):
            return book
    raise HTTPException(status_code=404, detail="Book not found!")

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def createBook(bookIn: BookIn):
    newBook = Book(**bookIn.dict())
    newBook.id = getNextBookId()
    books.append(newBook)
    return newBook

@app.put("/books/{id}")
async def updateBook(bookIn: BookIn, id: int = Path(gt=0)):
    for i in range(len(books)):
        if(books[i].id == id):
            editBook = Book(**bookIn.dict())
            editBook.id = id
            books[i] = editBook
            return books[i]
    raise HTTPException(status_code=404, detail="Book not found!")
        
@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def readBook(id: int = Path(gt=0)):
    for i in range(len(books)):
        if(books[i].id == id):
            books.pop(i)
            return
    raise HTTPException(status_code=404, detail="Book not found!")
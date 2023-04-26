from fastapi import Body, FastAPI

app = FastAPI()
lastBookId = 4
books = [
    {"id": 1, "title": "El señor de los anillos 1", "author": "R. Matt 1", "category": "ficcion"},
    {"id": 2, "title": "El señor de los anillos 2", "author": "R. Matt 2", "category": "ficcion"},
    {"id": 3, "title": "It", "author": "Melinda E.", "category": "terror"},
    {"id": 4, "title": "Finanzas Ninjas", "author": "Rodrigo R.", "category": "finanzas"},
]

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
async def readBook(id: int):
    for book in books:
        if(book.get("id") == id):
            return book
        
@app.post("/books")
async def createBook(newBook= Body()):
    newBook["id"] = len(books) + 1
    books.append(newBook)
    return newBook

@app.put("/books/{id}")
async def readBook(id: int, editBook= Body()):
    for i in range(len(books)):
        if(books[i].get("id") == id):
            editBook["id"] = id
            books[i] = editBook
            return books[i]

@app.delete("/books/{id}")
async def readBook(id: int):
    for i in range(len(books)):
        if(books[i].get("id") == id):
            books.pop(i)
            return True

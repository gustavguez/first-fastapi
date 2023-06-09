from fastapi import FastAPI
from routers import auth, books
from database.connection import engine
import tablemodels.book

app = FastAPI()
app.include_router(auth.router)
app.include_router(books.router)

tablemodels.book.Base.metadata.create_all(bind=engine)

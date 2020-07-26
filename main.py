from typing import Optional
import uuid
from fastapi import FastAPI
from pydantic import BaseModel, UUID4

app = FastAPI()


class Book(BaseModel):
    id: Optional[UUID4] = uuid.uuid4()
    name: str
    author: str
    availability: Optional[bool] = True
    label: str
    likes: int
    reads: int
    year: int
    ratings: float
    genre: Optional[str] = "Motivation"


static_books_db: dict = {}


@app.get("/")
def read_root():
    return {"message": "Welcome to Quidax Book API"}


@app.get("/books")
def get_books():
    return static_books_db


@app.get("/book/{book_id}")
def read_book(book_id: UUID4, q: Optional[str] = None):
    return {"book": static_books_db[book_id]}


@app.post("/books/")
def add_book(book: Book):
    static_books_db[book.id] = book
    return book


@app.put("/book/{book_id}")
def update_book(book_id: int, book: Book):
    return {"book_name": book.name, "book": book}

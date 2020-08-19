from typing import Optional, Dict, Any, Union

from fastapi import Body, APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4

from database.book import retrieve_books, retrieve_book, insert_book, remove_book
from models.model import Book

router = APIRouter()


@router.get("/", response_description="Books retrieved.")
def get_books(*, q: Optional[str] = None) -> dict:
    # Implement a search that filter books based on a passed query, if any.
    return retrieve_books()


@router.get("/{id}", response_description="Book retrieved.")
def read_book(id) -> Dict[str, Any]:
    return retrieve_book(id)


@router.post("/", response_description="Book added into the shelf.")
def add_book(book: Book = Body(...)) -> Dict[str, Union[UUID4, Any]]:
    # Might later change it to form input when the frontend is ready.
    return insert_book(jsonable_encoder(book))


@router.delete("/{id}", response_description="Book deleted")
def delete_book(id) -> dict:
    remove_book(id)
    return {"message": "Book with id {} successfully deleted".format(id)}

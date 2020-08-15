import uuid
import secrets
from typing import Dict, Any, Union
from typing import Optional, List

from bson import ObjectId
from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import UUID4
from starlette import status

from database.database import insert_user, retrieve_users, retrieve_user
from helper.model import Book, UserModel
from helper.responses import success_response

app = FastAPI()
hash_helper = CryptContext(schemes=["bcrypt"])

static_books_db: dict = {}
users: dict = {}

security = HTTPBasic()

def validate_data(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "Youngestdev")
    correct_password = secrets.compare_digest(credentials.password, "password")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"}
        )
    return True

@app.get("/user/{id}", tags=["users"], response_description="User retrieved")
def get_user(id) -> dict:
    return retrieve_user(ObjectId(id)) # Fix the ObjectID stuff!

@app.get("/user", tags=["users"], response_description="Users retrieved")
def get_users():
    return retrieve_users()
    # I feel having this function looks odd tbh. I should refactor this after implementing database support completely TODO


@app.post("/user/new", tags=["users"], response_description="User Created")
def create_user(user: UserModel) -> Dict[str, Union[UUID4, dict]]:
    user.password = hash_helper.encrypt(user.password)
    return insert_user(jsonable_encoder(user))


@app.get("/", tags=["book"])
def read_root():
    return {"message": "Welcome to Quidax Book API"}


@app.get("/book", response_description="Books retrieved.", tags=["book"])
def get_books(*, q: Optional[str] = None) -> dict:
    # Implement a search that filter books based on a passed query, if any.
    books = []
    for _id in static_books_db.keys():
        books.append(static_books_db[_id])
    return success_response(books, 200, "Books retrieved") if books else success_response()


@app.get("/book/{id}", response_description="Book retrieved.", tags=["book"])
def read_book(id: UUID4) -> Dict[str, Any]:
    if id not in static_books_db:
        raise HTTPException(status_code=404, detail="Book is not in the shelf.")
    return {"book": static_books_db[id]}


@app.post("/book/", response_description="Book added into the shelf.", tags=["book"])
def add_book(book: Book = Body(...)) -> Dict[str, Union[UUID4, Any]]:
    # Might later change it to form input when the frontend is ready.
    book.id = uuid.uuid4()
    static_books_db[book.id] = jsonable_encoder(book)
    return static_books_db[book.id]


@app.put("/book/{id}", response_description="Book updated.", tags=["book"])
def update_book(id: UUID4, book: Book) -> Book:
    stored_book_data = static_books_db[id]
    stored_book_data_model = Book(**stored_book_data)
    updated_book_data = book.dict(exclude_unset=True)
    updated_book_data = stored_book_data_model.copy(update=updated_book_data)
    static_books_db[id] = jsonable_encoder(updated_book_data)
    return updated_book_data


@app.delete("/book/{id}", response_description="Book deleted.", tags=["book"])
def delete_book(id: UUID4 = Query(...)) -> dict:
    del static_books_db[id]
    return {"message": "Book with id {} successfully deleted".format(id)}


"""
The method below might be standalone - maybe - automatically triggered from the frontend
or we might just use cloudinary to save the stress of uploading from the backend.
"""


@app.post("/upload", tags=["book"])
def upload_book_cover(file: List[UploadFile] = File(...)) -> dict:
    return {"file": [f.filename for f in file]}

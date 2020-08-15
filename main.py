import secrets
from typing import Dict, Any, Union
from typing import Optional

from bson import ObjectId
from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import UUID4
from starlette import status

from database.database import insert_user, retrieve_users, retrieve_user, find_user, retrieve_books, retrieve_book, \
    insert_book, remove_book
from helper.model import Book, UserModel
from helper.responses import success_response, error_response

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

@app.post("/user/new", tags=["users"], response_description="User Created")
def create_user(user: UserModel) -> Dict[str, Union[UUID4, dict]]:
    if find_user(user.email):
        return error_response("Email has been used to register", 409)
    user.password = hash_helper.encrypt(user.password)
    return insert_user(jsonable_encoder(user))

@app.get("/", tags=["book"])
def read_root():
    return {"message": "Welcome to Quidax Book API, use the /docs route,"}

@app.get("/book", response_description="Books retrieved.", tags=["book"])
def get_books(*, q: Optional[str] = None) -> dict:
    # Implement a search that filter books based on a passed query, if any.
    return retrieve_books()


@app.get("/book/{id}", response_description="Book retrieved.", tags=["book"])
def read_book(id) -> Dict[str, Any]:
    return retrieve_book(id)


@app.post("/book/", response_description="Book added into the shelf.", tags=["book"])
def add_book(book: Book = Body(...)) -> Dict[str, Union[UUID4, Any]]:
    # Might later change it to form input when the frontend is ready.
    return insert_book(jsonable_encoder(book))

# TODO:
@app.put("/book/{id}", response_description="Book updated.", tags=["book"])
def update_book(id: UUID4, book: Book) -> Book:
    stored_book_data = static_books_db[id]
    stored_book_data_model = Book(**stored_book_data)
    updated_book_data = book.dict(exclude_unset=True)
    updated_book_data = stored_book_data_model.copy(update=updated_book_data)
    static_books_db[id] = jsonable_encoder(updated_book_data)
    return updated_book_data


@app.delete("/book/{id}", response_description="Book deleted.", tags=["book"])
def delete_book(id) -> dict:
    remove_book(id)
    return {"message": "Book with id {} successfully deleted".format(id)}


"""
The method below might be standalone - maybe - automatically triggered from the frontend
or we might just use cloudinary to save the stress of uploading from the backend.
"""


# @app.post("/upload", tags=["book"])
# def upload_book_cover(file: List[UploadFile] = File(...)) -> dict:
#     return {"file": [f.filename for f in file]}

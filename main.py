import uuid
from typing import Dict, Any, Union
from typing import Optional, List

from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Body
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from pydantic import UUID4

from helper.helpers import user_helper, check_duplicate
from helper.model import Book, UserModel
from helper.responses import succeess_response

app = FastAPI()
hash_helper = CryptContext(schemes=["bcrypt"])

static_books_db: dict = {}
users: dict = {}


@app.get("/user/{id}", tags=["users"], response_description="User retrieved")
def get_user(id: UUID4 = Query(...)) -> dict:
    if id in users:
        user = users[id]
        return user_helper(user)


@app.get("/user", tags=["users"], response_description="Users retrieved")
def get_users() -> Dict[str, Union[list, int, str]]:
    user_list = []
    for user_id in users.keys():
        user = users[user_id]
        user_list.append(user_helper(user))

    return succeess_response(user_list, 200, "Users returned") if user_list else succeess_response(user_list)


@app.post("/user/new", tags=["users"], response_description="User Created")
def create_user(user: UserModel) -> Dict[str, Union[UUID4, dict]]:
    if not check_duplicate(users, user.username):
        user.id = uuid.uuid4()
        user.password = hash_helper.encrypt(user.password)
        users[user.id] = user
        return get_user(user.id)
    return {}


@app.get("/", tags=["book"])
def read_root():
    return {"message": "Welcome to Quidax Book API"}


@app.get("/book", response_description="Books retrieved.", tags=["book"])
def get_books(*, q: Optional[str] = None) -> dict:
    # Implement a search that filter books based on a passed query, if any.
    books = []
    for _id in static_books_db.keys():
        books.append(static_books_db[_id])
    return succeess_response(books, 200, "Books retrieved") if books else succeess_response(books)


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

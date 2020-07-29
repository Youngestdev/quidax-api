import uuid
from typing import Dict, Any, Union
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Body, Depends
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from pydantic import BaseModel, HttpUrl, Field, EmailStr
from pydantic import UUID4

app = FastAPI()
hash_helper = CryptContext(schemes=["bcrypt"])

static_books_db: dict = {}
users: dict = {}


class Book(BaseModel):
    name: str
    author: str
    availability: Optional[bool] = True
    label: List[str]
    likes: int
    reads: int
    year: int
    rating: Optional[float] = 0.0  # Ratings should be calculated from the number of reads & likes, perhaps.
    genre: Optional[str] = "Motivation"
    book_cover: Optional[HttpUrl] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Dream Psychology",
                "author": "Sigmund Freud",
                "availability": True,
                "label": ["psychic", "dreams"],
                "likes": 100,
                "reads": 250,
                "year": 1883,
                "rating": 4.5,
                "genre": "psychology",
                "book_cover": "http://myfile.com/img/here"
            }
        }


class UserModel(BaseModel):
    username: str = Field(...)
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "Youngestdev",
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "youngestdev@gmail.com",
                "password": "12345"
            }
        }


def user_helper(user):
    return {
        "username": user.username,
        "full_name": user.fullname,
        "user_email": user.email
    }


def check_duplicate(username) -> bool:
    for uid in users.keys():
        _user = user_helper(users[uid])
        if _user["username"] == username:
            raise Exception("Username exists, do use another one.")
    return False


@app.get("/user/{uid}", tags=["users"], response_description="User retrieved")
def get_user(uid: UUID4 = Query(...)) -> dict:
    if uid in users:
        user = users[uid]
        return user_helper(user)


@app.get("/users", tags=["users"], response_description="Users retrieved")
def get_users() -> List:
    user_list = []
    for user_id in users.keys():
        user = users[user_id]
        user_list.append(user_helper(user))
    return user_list


@app.post("/users/new", tags=["users"], response_description="User Created")
def create_user(user: UserModel) -> Dict[str, Union[UUID4, dict]]:
    if not check_duplicate(user.username):
        user_id = uuid.uuid4()
        user.password = hash_helper.encrypt(user.password)
        users[user_id] = user
        return {"id": user_id, "user_data": get_user(user_id)}
    return {}


@app.get("/", tags=["book"])
def read_root():
    return {"message": "Welcome to Quidax Book API"}


@app.get("/books", response_description="Books retrieved.", tags=["book"])
def get_books(*, q: Optional[str] = None) -> dict:
    # Implement a search that filter books based on a passed query, if any.
    return {"books": [static_books_db]}


@app.get("/book/{book_id}", response_description="Book retrieved.", tags=["book"])
def read_book(book_id: UUID4) -> Dict[str, Any]:
    if book_id not in static_books_db:
        raise HTTPException(status_code=404, detail="Book is not in the shelf.")
    return {"book": static_books_db[book_id]}


@app.post("/books/", response_description="Book added into the shelf.", tags=["book"])
def add_book(book: Book = Body(...)) -> Dict[str, Union[UUID4, Any]]:
    # Might later change it to form input when the frontend is ready.
    bid = uuid.uuid4()
    static_books_db[bid] = jsonable_encoder(book)
    return {"book_id": bid, "book_details": static_books_db[bid]}


@app.put("/book/{book_id}", response_description="Book updated.", tags=["book"])
def update_book(book_id: UUID4, book: Book) -> Book:
    stored_book_data = static_books_db[book_id]
    stored_book_data_model = Book(**stored_book_data)
    updated_book_data = book.dict(exclude_unset=True)
    updated_book_data = stored_book_data_model.copy(update=updated_book_data)
    static_books_db[book_id] = jsonable_encoder(updated_book_data)
    return updated_book_data


@app.delete("/book/{book_id}", response_description="Book deleted.", tags=["book"])
def delete_book(book_id: UUID4 = Query(...)) -> dict:
    del static_books_db[book_id]
    return {"message": "Book with id {} successfully deleted".format(book_id)}


"""
The method below might be standalone - maybe - automatically triggered from the frontend
or we might just use cloudinary to save the stress of uploading from the backend.
"""


@app.post("/upload", tags=["book"])
def upload_book_cover(file: List[UploadFile] = File(...)) -> dict:
    return {"file": [f.filename for f in file]}

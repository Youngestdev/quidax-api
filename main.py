import uuid
from typing import Optional, List, Dict, Any, Tuple, Union
from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, UUID4, HttpUrl, EmailStr, Field
from passlib.context import CryptContext


app = FastAPI()
hash_helper = CryptContext(schemes=["bcrypt"])


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


static_books_db: dict = {}
users: dict = {}


@app.get("/user/{uid}", tags=["users"], response_description="User retrieved")
def get_users(uid: UUID4 = Query(...)) -> dict:
    if uid in users:
        user = users[uid]
        return user_helper(user)


@app.post("/users/new", tags=["users"], response_description="User Created")
def create_user(user: UserModel) -> Dict[str, Union[UUID4, UserModel]]:
    user_id = uuid.uuid4()
    user.password = hash_helper.encrypt(user.password)
    users[user_id] = user
    return {"id": user_id, "user_data": user}


@app.get("/", tags=["book"])
def read_root():
    return {"message": "Welcome to Quidax Book API"}


@app.get("/books", response_description="Books retrieved.", tags=["book"])
def get_books(*, q: Optional[str] = None) -> dict:
    # Implement a search that filter books based on a passed query, if any.
    return {"books": static_books_db}


@app.get("/book/{book_id}", response_description="Book retrieved.", tags=["book"])
def read_book(book_id: UUID4) -> Dict[str, Any]:
    if book_id not in static_books_db:
        raise HTTPException(status_code=404, detail="Book is not in the shelf.")
    return {"book": static_books_db[book_id]}


@app.post("/books/", response_description="Book added into the shelf.", tags=["book"])
def add_book(book: Book = Body(...)) -> Book:
    # Might later change it to form input when the frontend is ready.
    bid = uuid.uuid4()
    static_books_db[bid] = jsonable_encoder(book)
    return static_books_db[bid]


@app.patch("/book/{book_id}", response_description="Book updated.", tags=["book"])
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

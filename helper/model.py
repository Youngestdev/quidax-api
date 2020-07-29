from typing import Optional, List

from pydantic import BaseModel, HttpUrl, EmailStr, Field, UUID4


class Book(BaseModel):
    id: UUID4 = Field(default=None)
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
    id: UUID4 = Field(default=None)
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

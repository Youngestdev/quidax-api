from bson import ObjectId
from pydantic import EmailStr
from pymongo import MongoClient
from decouple import config

from helper.helpers import user_helper, book_helper
from helper.responses import success_response

MONGO_DEETS = config('MONGO_DEETS')

client = MongoClient(MONGO_DEETS)

database = client.quidax
book_collection = database.books
user_collection = database.users

# TODO: Retreive data, post data. Basically CRUD!

def insert_user(user_data: dict) -> dict:
    id = user_collection.insert(user_data)
    new_user = user_collection.find_one({"_id": id})
    return success_response(book_helper(new_user), 200, "Book successfully added into the database")

def insert_book(book_data: dict) -> dict:
    id = book_collection.insert(book_data)
    new_book = book_collection.find_one({"_id": id})
    return success_response(book_helper(new_book), 200, "User successfully added into the database")

def retrieve_users() -> dict:
    users = list(user_collection.find({}))
    userlist = []
    for user in users:
        userlist.append(user_helper(user))
    return success_response(userlist, 200, "Users retrieved.") if userlist else success_response()

def retrieve_books() -> dict:
    books = list(book_collection.find({}))
    booklist = []
    for book in books:
        booklist.append(book_helper(book))
    return success_response(booklist, 200, "Books retrieved.") if booklist else success_response()

def retrieve_user(id: ObjectId) -> dict:
    user = user_collection.find_one({"_id": id})
    return success_response(user_helper(user), 200, "User Retrieved") if user else success_response()

def retrieve_book(id: ObjectId) -> dict:
    user = book_collection.find_one({"_id": id})
    return success_response(book_helper(user), 200, "Book Retrieved") if user else success_response()

def find_user(email: EmailStr) -> bool:
    user = user_collection.find_one({"email": email})
    if user:
        return True
    return False

def remove_book(id: ObjectId):
    return book_collection.delete_one({"_id": ObjectId(str(id))})
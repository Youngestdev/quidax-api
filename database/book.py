from bson import ObjectId

from database.database import book_collection
from helper.helpers import book_helper
from helper.responses import success_response


def insert_book(book_data: dict) -> dict:
    id = book_collection.insert(book_data)
    new_book = book_collection.find_one({"_id": id})
    return success_response(book_helper(new_book), 200, "User successfully added into the database")

def retrieve_books() -> dict:
    books = list(book_collection.find({}))
    booklist = []
    for book in books:
        booklist.append(book_helper(book))
    return success_response(booklist, 200, "Books retrieved.") if booklist else success_response()

def retrieve_book(id: ObjectId) -> dict:
    user = book_collection.find_one({"_id": id})
    return success_response(book_helper(user), 200, "Book Retrieved") if user else success_response()

def remove_book(id: ObjectId):
    return book_collection.delete_one({"_id": ObjectId(str(id))})

def update_book(id: ObjectId):
    pass
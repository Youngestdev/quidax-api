from bson import ObjectId
from pydantic import EmailStr

from database.database import user_collection
from helper.helpers import user_helper
from helper.responses import success_response


def insert_user(user_data: dict) -> dict:
    id = user_collection.insert(user_data)
    new_user = user_collection.find_one({"_id": id})
    return success_response(user_helper(new_user), 200, "User successfully added into the database")

def retrieve_users() -> dict:
    users = list(user_collection.find({}))
    userlist = []
    for user in users:
        userlist.append(user_helper(user))
    return success_response(userlist, 200, "Users retrieved.") if userlist else success_response()

def retrieve_user(id: ObjectId) -> dict:
    user = user_collection.find_one({"_id": id})
    return success_response(user_helper(user), 200, "User Retrieved") if user else success_response()

def find_user(email: EmailStr) -> bool:
    user = user_collection.find_one({"email": email})
    if user:
        return True
    return False
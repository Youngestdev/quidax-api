from pymongo import MongoClient
from decouple import config

from helper.helpers import user_helper
from helper.responses import success_response

MONGO_DEETS = config('MONGO_DEETS')

client = MongoClient(MONGO_DEETS)

database = client.quidax
book_collection = database.books
user_collection = database.users

# book = {
#   "name": "Dream Psychology",
#   "author": "Sigmund Freud",
#   "availability": True,
#   "label": [
#     "psychic",
#     "dreams"
#   ],
#   "likes": 100,
#   "reads": 250,
#   "year": 1883,
#   "rating": 4.5,
#   "genre": "psychology",
#   "book_cover": "http://myfile.com/img/here"
# }
#
# result = book_collection.insert(book)
# print('One post ID: {0}'.format(result))

# TODO: Retreive data, post data. Basically CRUD!

def insert_user(user_data):
    id = user_collection.insert(user_data)
    print("New user ID: ", id)
    new_user = user_collection.find_one({"_id": id})
    return success_response(user_helper(new_user), 200, "User successfully added into the database")
#
def retrieve_users():
    users = list(user_collection.find({}))
    userlist = []
    for user in users:
        userlist.append(user_helper(user))
    return success_response(userlist, 200, "Users retrieved.") if userlist else success_response()

def retrieve_user(id):
    user = user_collection.find_one({"_id": id})
    print(user)
    return success_response(user_helper(user), 200, "User Retrieved") if user else success_response()
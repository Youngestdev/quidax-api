from pymongo import MongoClient

from helper.helpers import user_helper

client = MongoClient('localhost', 27018)

database = client.QUIDAX
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
    return "Okay"

def retrieve_users():
    users = list(user_collection.find({}))
    userlist = []
    for user in users:
        userlist.append(user_helper(user))
    return userlist
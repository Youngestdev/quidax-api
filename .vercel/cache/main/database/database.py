from pymongo import MongoClient
from decouple import config

MONGO_DEETS = config('MONGO_DEETS')

client = MongoClient(MONGO_DEETS)

database = client.quidax
book_collection = database.books
user_collection = database.users

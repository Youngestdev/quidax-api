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

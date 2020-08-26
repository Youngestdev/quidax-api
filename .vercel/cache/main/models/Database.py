import json
from typing import List

from database.database import database

# class Database:
#     def __init__(self, collection):
#         self.db = database
#         self.collection = collection
#         print("Collection valaue: ", self.collection)
#
#     def retrieve(self, helper):
#         data = self.db[self.collection].find({})
#
#         print(data)
#         print("Data: ", data)
#         return data
#
#     def get(self, id):
#         data = self.db.collection.find({"_id": id})
#
#         return data
from database.user import retrieve_users


class Database:
    def __init__(self):
        self.db: List = retrieve_users().get('data')
        self.users = [user['id'] for user in self.db]

    def retrieve(self):
        return self.users
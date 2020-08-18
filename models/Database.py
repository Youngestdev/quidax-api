from database.database import database

class Database:
    def __init__(self, collection):
        self.db = database

    def retrieve(self, helper):
        data = list(self.db.collection.find({}))
        data = [helper(_data) for _data in data]
        return data

    def get(self, id):
        data = self.db.collection.find({"_id": id})

        return data
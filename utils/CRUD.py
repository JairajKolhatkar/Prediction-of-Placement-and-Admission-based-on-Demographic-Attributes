from pymongo import MongoClient


class CRUD:
    # Constructor
    def __init__(self, database_name, collection_name):
        self.client = MongoClient()
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    # insert data
    def create(self, data):
        return self.collection.insert_one(data)

    # Read data
    def read(self, query):
        return self.collection.find(query)

    # Check data
    def check_data(self, query):
        return self.collection.find_one(query)

    # Update data
    def update(self, query, new_data):
        return self.collection.update_one(query, {"$set": new_data})

   # Delete data
    def delete(self, query):
        return self.collection.delete_one(query)

   #Add features to database
    def add_features(self,query):
     ...
#!/usr/bin/env python3
"""The engine for the NoSQL
MongoDB
"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()
mongodb_host = os.getenv('MONGODB_HOST')
mongodb_port = os.getenv('MONGODB_PORT')
mongodb_name = os.getenv('MONGODB_NAME')

class MongoDBstorage:
    """Defines the mongodb engine and
    CRUD operations
    """
    __db = None
    __client = None

    def __init__(self):
        """Initializes the mongodb 
        database
        """
        self.__client = MongoClient(f"mongodb://{mongodb_host}:{mongodb_port}")
        self.__db = self.__client[mongodb_name]

    def switch_db(self, database):
        """switches to the 'database'
        """
        self.__db = self.__client[database]

    def create_col(self, collection_name):
        """Createes a collection 
        'collection_name'
        """
        self.__db.create_collection(collection_name)

    def insert_one(self, collection_name, data):
        """Inserts a single data into the datase
        """
        collection = self.__db[collection_name]
        return collection.insert_one(data)
    
    def insert_many(self, collection_name, data_list):
        """Inserts multiple data into the databse
        """
        collection = self.__db[collection_name]
        return collection.insert_many(data_list)

    def find(self, collection_name, query=None):
        """Searches or finds data in the database
        """
        collection = self.__db[collection_name]
        return collection.find(query)
    
    def count(self, collection_name):
        """Counts the number of documents in a collection"""
        collection = self.__db[collection_name]
        return collection.count_documents({})

    def update_one(self, collection_name, query, new_values):
        """Updates the database with a single data
        """
        collection = self.__db[collection_name]
        return collection.update_one(query, {"$push": new_values})
    
    def update_many(self, collection_name, query, new_values):
        """Updates the database with multiple data
        """
        collection = self.__db[collection_name]
        return collection.update_many(query, {"$set": new_values})

    def delete_one(self, collection_name, query):
        """deletes data from the databse
        """
        collection = self.__db[collection_name]
        return collection.delete_one(query)
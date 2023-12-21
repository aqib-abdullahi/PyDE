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
        self.__client = MongoClient(mongodb_host, mongodb_port)
        self.__db = self.__client[mongodb_name]

    def switch_db(self, database):
        self.__db = self.__client[database]

    def create_col(self, collection_name):
        self.__db.create_collection(collection_name)

    def insert_one(self, collection_name, data):
        collection = self.__db[collection_name]
        return collection.insert_one(data)
    
    def insert_many(self, collection_name, data_list):
        collection = self.__db[collection_name]
        return collection.insert_many(data_list)

    def find(self, collection_name, query=None):
        collection = self.__db[collection_name]
        return collection.find(query)

    def update_one(self, collection_name, query, new_values):
        collection = self.__db[collection_name]
        return collection.update_one(query, {"$set": new_values})
    
    def update_many(self, collection_name, query, new_values):
        collection = self.__db[collection_name]
        return collection.update_many(query, {"$set": new_values})

    def delete_one(self, collection_name, query):
        collection = self.__db[collection_name]
        return collection.delete_one(query)
#!/usr/bin/env python3
"""initializes models package
and mysqldb engine"""
from app.models.engine.mysql import MySQLDBstorage
from app.models.engine.mongodb import MongoDBstorage


storage = MySQLDBstorage()
storage.reload()

mongodb_store = MongoDBstorage()
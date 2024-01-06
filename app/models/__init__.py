#!/usr/bin/env python3
"""initializes models package
and mysqldb engine"""
from app.models.engine.mysql import MySQLDBstorage
from app.models.engine.mongodb import MongoDBstorage
from app.models.engine.dockerSDK import dockerSDK


storage = MySQLDBstorage()
storage.reload()

mongodb_store = MongoDBstorage()
dockerEngine = dockerSDK()
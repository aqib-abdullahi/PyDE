# from models.engine.mysql import MySQLDBstorage
"""initializes models package"""
from app.models.engine.mysql import MySQLDBstorage

storage = MySQLDBstorage()
storage.reload()
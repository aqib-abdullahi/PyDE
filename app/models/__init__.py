#!/usr/bin/env python3
"""initializes models package
and mysqldb engine"""
from app.models.engine.mysql import MySQLDBstorage

storage = MySQLDBstorage()
storage.reload()
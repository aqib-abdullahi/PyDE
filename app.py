#!/usr/bin/env python3
"""Main app entry point
"""
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from app.models.user import User
from app.models import storage
from app.main.main import main
from app.auth.auth import auth
from app.auth.db import authDB
from app.models import mongodb_store


app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecret'
login_manager = LoginManager()
login_manager.init_app(app)
cors = CORS(app)
app.register_blueprint(main)
app.register_blueprint(auth)

@login_manager.user_loader
def user_loader(user_id):
    """Given 'user_id', returns associated
    User object
    """
    authenticateDB = authDB()
    user = authenticateDB.retrieve_user(user_id)
    return user

if __name__ == "__main__":
    app.run(debug=True)
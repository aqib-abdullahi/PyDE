#!/usr/bin/env python3
"""main module
containing main page
"""
from flask import Flask, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user, login_user
from dotenv import load_dotenv
import os
import json
import requests
from app.models.user import User
from app.models import mongodb_store
from app.auth.auth import authDB


main = Blueprint('main', __name__)
load_dotenv()


def initialize_file_tree(user_id):
    """Initializes a database for the user with the user id"""
    default_root = {
        "name": "PyDE",
        "type": "folder",
        "parent_folder": None,
        "user_id": user_id,
        "children": [],
    }
    finder = mongodb_store.find("files", {"name": "PyDE", "type": "folder", "user_id": user_id})
    result = list(finder)
    if len(result) == 0:
        inserted = mongodb_store.insert_one("files", default_root)
        return inserted.inserted_id

@login_required
@main.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Main page
    """
    ip_address = os.getenv('IP_ADDRESS')
    container_id = current_user.Container
    container_port = os.getenv('CONTAINER_PORT')
    user_id = current_user.get_id()
    if current_user.is_authenticated:
        id = current_user.get_id()
        initialize_file_tree(id)
        response = requests.get(f"http://127.0.0.1:5000/api/v1/users/{current_user.get_id()}/files")
        file_tree = response.json()
        return render_template('IDE.html',
                            ip_address=ip_address,
                            user_id = user_id,
                            container_id=container_id,
                            container_port=container_port,
                            file_tree = file_tree)
    else:
        from app.auth.auth import auth
        return redirect(url_for('auth.login'))
    
# @login_required
@main.route('/file-tree', methods=['GET'], strict_slashes=False)
def file_tree_process():
    """renders the file_tree html"""
    response = requests.get(f"http://127.0.0.1:5000/api/v1/users/{current_user.get_id()}/files")
    file_tree = response.json()
    return render_template('macros.html', file_tree=file_tree)
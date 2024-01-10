#!/usr/bin/env python3
"""Database file tree storage
"""
from flask import jsonify
from flask import Blueprint, request, render_template
from app.models import mongodb_store
from bson.objectid import ObjectId
from flask_login import current_user
from datetime import datetime
import requests

api_v1_users = Blueprint('api_v1_users', __name__)

@api_v1_users.route('/<user_id>/file-tree', methods=['GET'], strict_slashes=False)
def file_tree_process(user_id):
    """renders the file_tree html"""
    response = requests.get(f"http://127.0.0.1:5000/api/v1/users/{user_id}/files")
    file_tree = response.json()
    return render_template('macros.html', file_tree=file_tree)

@api_v1_users.route('/<user_id>/files', methods=['GET'], strict_slashes=False)
def get_files(user_id):
    """Gets all files and folders for a particular
    user
    """
    usersid = int(user_id)
    query = {"user_id": usersid}
    data =  list(mongodb_store.find("files", query))
    for item in data:
        if '_id' in item:
            item['_id'] = str(item['_id'])
    response_data = next((item for item in data if item.get('name') == 'PyDE'), None)
    return jsonify(response_data)

@api_v1_users.route('/<user_id>/files/<file_id>', methods=['GET'], strict_slashes=False)
def get_file(user_id, file_id):
    """gets a file based on its id"""
    usersid = int(user_id)
    query = {"user_id": usersid}
    files = list(mongodb_store.find("files", query))
    for file in files:
        children = file.get('children', [])
        for child in children:
            if child['_id'] == file_id:
                return jsonify(child)

    return jsonify({"message": "'mll' file not found"}), 404

@api_v1_users.route('/<user_id>/files', methods=['POST'], strict_slashes=False)
def create_file(user_id):
    """creates a file for a particular user
    """
    data = request.json
    file_name = data.get('file_name')
    folder_name = data.get('folder_name')
    file_contents = data.get('file_contents')
    parent_folder_id = data.get('parent_folder_id')
    if not file_name and not folder_name:
        return jsonify({'message': 'File or folder name is required'}), 400
    
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    try:
        file_data = {
                'user_id': user_id,
                '_id': str(ObjectId()),
                'name': file_name,
                'file_contents': file_contents,
                'folder_name': folder_name,
                'parent_folder_id': parent_folder_id,
                'children': [],
                'created_at': data['created_at'],
                'updated_at': data['updated_at']
        }
        updated = mongodb_store.update_one(
                "files",
                {"_id": ObjectId(parent_folder_id), "user_id": 15},
                {"children": file_data}
            )
        return jsonify({'message': 'File created successfully',
                        'id': file_data.get('_id')}), 200
    except Exception as e:
        return jsonify({"mesage": str(e)}), 500

@api_v1_users.route('/<user_id>/files/<file_id>', methods=['DELETE'], strict_slashes=False)
def delete_file(user_id, file_id):
    """deletes a file for a particular user
    using the file id"""
    usersid = int(user_id)
    query = {'user_id': usersid}
    try:
        mongodb_store.delete_one("files", query)
        return jsonify({'message': 'File deleted successfully', 'file': file_id}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 404

@api_v1_users.route('/<user_id>/files/<file_id>', methods=['PUT'], strict_slashes=False)
def update_file(user_id, file_id):
    """Updates the content of a file owned by a specific user"""
    data = request.json
    file_contents = data.get('file_contents')
    query = {"user_id": int(user_id), "children._id": file_id}
    update_data = {
        "children.$.file_contents": file_contents,
        "children.$.updated_at": datetime.now()
    }

    updated = mongodb_store.update_one_set("files", query, update_data)

    if updated.modified_count > 0:
        updated_document = mongodb_store.find("files", query)
        return jsonify({"message": "file updated successfully"}), 200

    return jsonify({'message': 'Failed to update file'}), 404

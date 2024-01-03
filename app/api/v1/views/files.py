#!/usr/bin/env python3
"""Database file tree storage
"""
from flask import jsonify
from flask import Blueprint, request
from app.models import mongodb_store
from bson.objectid import ObjectId
from flask_login import current_user
from datetime import datetime

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/users/<user_id>/files', methods=['GET'], strict_slashes=False)
def get_files(user_id):
    """Gets all files and folders for a particular
    user
    """
    query = {'user_id': user_id}
    data =  list(mongodb_store.find("files", query))
    print(data)
    for item in data:
        if '_id' in item:
            item['_id'] = str(item['_id'])

    return jsonify({'files': data})

@api_v1.route('/users/<user_id>/files', methods=['POST'], strict_slashes=False)
def create_file(user_id):
    """creates a file for a particular user
    """
    data = request.json
    file_name = data.get('file_name')
    folder_name = data.get('folder_name')
    file_contents = data.get('file_contents')
    parent = data.get('parent_folder')
    if not file_name and not folder_name:
        return jsonify({'message': 'File or folder name is required'}), 400
    
    data['created_at'] = datetime.now()
    data['updated_at'] = datetime.now()
    data['user_id'] = current_user.get_id()
    try:
        inserted = mongodb_store.insert_one("files",
                                            {
                                                'user_id': user_id,
                                                'file_name': file_name,
                                                'file_contents': file_contents,
                                                'folder_name': folder_name,
                                                'parent_folder': parent,
                                                'created_at': data['created_at'],
                                                'updated_at': data['updated_at']
                                            })
        return jsonify({'message': 'File created successfully',
                        'id': str(inserted.inserted_id)}), 201
    except Exception as e:
        return jsonify({"mesage": str(e)}), 500

@api_v1.route('/users/<user_id>/files/<file_id>', methods=['DELETE'], strict_slashes=False)
def delete_file(user_id, file_id):
    """deletes a file for a particular user
    using the file id"""
    query = {'user_id': user_id, '_id': ObjectId(file_id)}
    try:
        mongodb_store.delete_one("files", query)
        return jsonify({'message': 'File deleted successfully', 'file': file_id}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 404

@api_v1.route('/users/<user_id>/files/<file_id>', methods=['PUT'], strict_slashes=False)
def update_file(user_id, file_id):
    """Updates the content of a file owned by a
    specific user
    """
    query = {'user_id': user_id, '_id': ObjectId(file_id)}
    data = request.json
    file_contents = data.get('file_contents')
    updates = {'file_contents': file_contents, 'updated_at': datetime.now()}
    try:
        mongodb_store.update_one("files", query, updates)
        return jsonify({'message': 'File updated successfully', 'file': file_id}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 404
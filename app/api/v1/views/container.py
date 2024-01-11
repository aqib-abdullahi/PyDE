#!/usr/bin/env python3
"""container interaction API
"""
from flask import jsonify
from flask import Blueprint, request
from flask_login import current_user
from datetime import datetime
from app.models import dockerEngine


api_v1_container = Blueprint("api_v1_container", __name__)

@api_v1_container.route('/<user_id>/<container_id>', methods=['POST'], strict_slashes=False)
def upload_file(user_id, container_id):
    """uploads file to container as executable"""
    data = request.json
    file_contents = data.get('file_contents')
    file_name = data.get('name')

    result = dockerEngine.upload_file(container_id=container_id,
                                      file_content=file_contents,
                                      file_name=file_name)
    print(result)
    if result is not None:
        return jsonify({"message": "file uploaded"}), 200
    return jsonify({"message": "failed to upload"}), 422

@api_v1_container.route('/<user_id>/<container_id>/<file_name>', methods=['GET'], strict_slashes=False)
def execute_file(user_id, container_id, file_name):
    """eexecutes file inside container
    """
    result = dockerEngine.execute_file(container_id=container_id,
                                       file_name=file_name)
    if result is not None:
        return jsonify({"message": result}), 200
    return jsonify({"": ""}), 422

@api_v1_container.route('/<user_id>/<container_id>/<file_id>/<file_name>', methods=['PUT'], strict_slashes=False)
def update_file(user_id, container_id, file_id, file_name):
    """updates file already in container as executable"""
    data = request.json
    file_contents = data.get('file_contents')

    result = dockerEngine.upload_file(container_id=container_id,
                                      file_content=file_contents,
                                      file_name=file_name)
    print(result)
    if result is not None:
        return jsonify({"message": "file uploaded"}), 200
    return jsonify({"message": "failed to upload"}), 422
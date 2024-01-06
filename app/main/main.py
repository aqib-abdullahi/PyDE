#!/usr/bin/env python3
"""main module
containing main page
"""
from flask import Flask, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user, login_user
from dotenv import load_dotenv
import os
from app.models.user import User
from app.models import mongodb_store
from app.auth.auth import authDB

main = Blueprint('main', __name__)
load_dotenv()

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
        return render_template('IDE.html',
                            ip_address=ip_address,
                            user_id = user_id,
                            container_id=container_id,
                            container_port=container_port)
    else:
        from app.auth.auth import auth
        return redirect(url_for('auth.login'))
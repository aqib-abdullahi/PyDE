#!/usr/bin/env python3
"""main module
containing main page
"""
from flask import Flask, render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from dotenv import load_dotenv
import os
from app.models.user import User
from app.auth.auth import auth
from app.models import mongodb_store


main = Blueprint('main', __name__)
load_dotenv()


@main.route('/')
@login_required
def index():
    """Main page
    """
    ip_address = os.getenv('IP_ADDRESS')
    container_id = os.getenv('CONTAINER_ID')
    container_port = os.getenv('CONTAINER_PORT')
    if current_user.is_authenticated:
        return render_template('IDE.html',
                            ip_address=ip_address,
                            container_id=container_id,
                            container_port=container_port)
    return redirect(url_for('auth.login'))
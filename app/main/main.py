#!/usr/bin/env python3
"""main module
containing main page
"""
from flask import Flask, render_template, Blueprint
from dotenv import load_dotenv
import os


main = Blueprint('main', __name__)
load_dotenv()


@main.route('/')
def index():
    """Main page
    """
    ip_address = os.getenv('IP_ADDRESS')
    container_id = os.getenv('CONTAINER_ID')
    container_port = os.getenv('CONTAINER_PORT')
    
    return render_template('IDE.html',
                           ip_address=ip_address,
                           container_id=container_id,
                           container_port=container_port)
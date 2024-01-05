#!/usr/bin/env python3
"""authentication module
"""
from flask import Blueprint, request, render_template, redirect, url_for
from passlib.hash import bcrypt_sha256
from app.models import storage
from app.models.user import User
from app.auth.db import authDB
from app.models.engine.mysql import MySQLDBstorage
from flask_login import login_user,current_user, login_required, logout_user
import docker
import os
from dotenv import load_dotenv


load_dotenv()
ip = os.getenv('IP_ADDRESS')
remote_docker_client = docker.DockerClient(
    base_url = "tcp://172.20.10.2:2375"
)
auth = Blueprint('auth', __name__)

@auth.route('/Signup', methods=['GET', 'POST'], strict_slashes=False)
def Signup():
    """Logs user into signed up account
    """
    if request.method == 'GET':
        return render_template('signup.html', email_exists=False)
    elif request.method == 'POST':
        FirstName = request.form['First name']
        LastName = request.form['Last name']
        Email = request.form['Email']
        Password = request.form['Password']
        Container = str(FirstName)
        Repeat_password = request.form['Confirm password']

        authenticateDB = authDB()
        Password = authenticateDB.hash_password(Password)
        user = authenticateDB.add_user(FirstName=FirstName,
                        LastName=LastName,
                        Email=Email,
                        Password=Password,
                        Container=Container,
                        Authenticated=False)
        if (user == "user exists"):
            email_exists = True
            return render_template('signup.html', email_exists=email_exists)
        elif user:
            container_id = remote_docker_client.containers.run('python-container',
                                                command="/bin/bash",
                                                name=Container,
                                                stdin_open=True,
                                                tty=True,
                                                detach=True)
            print(container_id)

            py_version = container_id.exec_run("python --version")
            print(py_version)
            # update package
            # update_command = "apt-get update"
            # update_result = container_id.exec_run(update_command)
            # print(update_result.output.decode('utf-8'))

            # Install python3
            # install = "apt-get install -y python3"
            # install_result = container_id.exec_run(install)
            # print(install_result.output.decode('utf-8'))
            return redirect(url_for('auth.login'))
    
@auth.route('/Login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'GET':
        return render_template('login.html', form_data=None)
    elif request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']

        session = storage.get_session()
        user = session.query(User).filter_by(Email = email).first()
        session.close()
        authenticateDB = authDB()
        verified_user = authenticateDB.verify_user(email, password)
        if verified_user is not None:
            session = storage.get_session()
            try:
                user.Authenticated = True
                storage.new(user)
                storage.save()
                login_user(user, remember=False)
                from app.main.main import main
                return redirect(url_for('main.index'))
            except Exception as e:
                print(e)
                session.rollback()
                session.close()
                form_data = {
                "Email": email
                }
                return render_template('login.html', form_data=form_data)
        else:
            form_data = {
                "Email": email
            }
            return render_template('login.html', form_data=form_data)

@auth.route('/Logout', methods=['GET', 'POST'], strict_slashes=False)
def logout():
    """Logs out the user from the session
    """
    if current_user.is_authenticated:
        user = current_user
        session = storage.get_session()
        try:
            user.Authenticated = False
            storage.new(user)
            storage.save()
        except Exception as e:
            session.rollback()
            session.close()
        logout_user()
        return redirect(url_for('auth.login'))

    return redirect(url_for('auth.login'))
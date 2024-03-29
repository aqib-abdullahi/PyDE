#!/usr/bin/env python3
"""authentication module
"""
import uuid
from flask import Blueprint, request, render_template, redirect, url_for
from passlib.hash import bcrypt_sha256
from app.models import storage, dockerEngine
from app.models.user import User
from app.auth.db import authDB
from app.models.engine.mysql import MySQLDBstorage
from flask_login import login_user,current_user, login_required, logout_user


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
        Container = str(uuid.uuid4())
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
            container_id = dockerEngine.spawn_container(Container)
            session = storage.get_session()
            user = session.query(User).filter_by(Email = Email).first()
            session.close()
            try:
                container = str(container_id)
                containerID = container.split(': ')[1][:-1]
                user.Container = containerID
                storage.new(user)
                storage.save()
            except Exception as e:
                print(e)
                session.rollback()
                session.close()

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
                return redirect(url_for('main.IDE'))
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

@login_required
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
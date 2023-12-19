"""authentication module
"""
from app.models.engine.mysql import MySQLDBstorage
from flask import Blueprint, request, render_template, redirect, url_for
from passlib.hash import bcrypt_sha256
from app.models import storage
from app.models.user import User
from app.auth.db import authDB
# from ....PyDE import app
from flask_login import login_user,current_user, login_required, logout_user


auth = Blueprint('auth', __name__)

@auth.route('/Signup', methods=['GET', 'POST'], strict_slashes=False)
def Signup():
    """Logs user into signed up account
    """
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        FirstName = request.form['First name']
        LastName = request.form['Last name']
        Email = request.form['Email']
        Password = request.form['Password']
        Repeat_password = request.form['Confirm password']

        authenticateDB = authDB()
        Password = authenticateDB.hash_password(Password)
        user = authenticateDB.add_user(FirstName=FirstName,
                        LastName=LastName,
                        Email=Email,
                        Password=Password,
                        Container="None yet",
                        Authenticated=False)
        if user:
            return render_template('login.html')
        
        return render_template('signup.html')
    
@auth.route('/Login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']

        session = storage.get_session()
        user = session.query(User).filter_by(Email = Email).first()
        session.close()
        authenticateDB = authDB()
        verified_user = authenticateDB.verify_user(Email,Password)
        if verified_user:
            session = storage.get_session()
            user.Authenticated = True
            try:
                storage.new(user)
                storage.save()
            except Exception as e:
                print(e)
                session.rollback()
                session.close()
            
            login_user(user, remember=False)
            # return redirect(url_for('signup'))
            return render_template('IDE.html')
        else:
            return render_template('login.html')
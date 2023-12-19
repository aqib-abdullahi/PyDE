"""authentication module
"""
from app.models.engine.mysql import MySQLDBstorage
from flask import Blueprint, request, render_template
from passlib.hash import bcrypt_sha256
from app.models import storage
from app.models.user import User
from app.auth.db import authDB


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
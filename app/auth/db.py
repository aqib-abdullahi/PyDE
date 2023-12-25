#!/usr/bin/env python3
"""database; users
authentication
"""
from passlib.hash import bcrypt_sha256
from app.models import storage
from app.models.user import User
from flask_login import login_user


class authDB:
    """authdb class:
    accessing databse for authentication
    """
    def hash_password(self, password):
        """hashes a passed passed to the function
        """
        hashed = bcrypt_sha256.hash(password)
        return hashed
    
    def user_exist(self, Email):
        """returns true if email exists in database
        """
        session = storage.get_session()
        user = session.query(User).filter_by(Email = Email).first()
        session.close()
        if user:
            return True
        return False
    
    def add_user(self,
                 FirstName,
                 LastName,
                 Email,
                 Password,
                 Container,
                 Authenticated):
        """ Adds user to db
        returns user object
        """
        user = None
        user_exists = self.user_exist(Email=Email)
        if user_exists:
            return "user exists"
        else:
            try:
                hashed_password = self.hash_password(Password)
                user = User(FirstName=FirstName,
                            LastName=LastName,
                            Email=Email,
                            Password=hashed_password,
                            Container=Container,
                            Authenticated=Authenticated)
                session = storage.get_session()
                storage.new(user)
                storage.save()
            except Exception as e:
                print(e)
                session.rollback()
                user = None
            return user

    def verify_user(self, email, password):
        """Verifies the existence of user with the
        given parameters"""
        session = storage.get_session()
        user = session.query(User).filter_by(Email = email).first()
        session.close()
        if user:
            user_hashed = user.Password
            if user_hashed is not None:
                hashed_password = user_hashed
                validity = bcrypt_sha256.verify(password, user_hashed)
                if validity is not None:
                    return True
                else:
                    return False
            else:
                return False
        return False
    
    def retrieve_user(self, user_id):
        """returns user object based on the
        passed userID
        """
        session = storage.get_session()
        user = session.query(User).get(user_id)
        session.close()
        return user
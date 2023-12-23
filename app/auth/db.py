#!/usr/bin/env python3
"""database; users
authentication
"""
from app.models.user import User
from passlib.hash import bcrypt_sha256
from app.models import storage


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

    def verify_user(self, Email, Password):
        """Verifies the existence of user with the
        given parameters"""
        session = storage.get_session()
        user = session.query(User).filter_by(Email = Email).first()
        session.close()
        if user:
            session = storage.get_session()
            user_hashed = session.query(User).filter(User.Email == Email).first()
            session.close
            if user_hashed:
                hashed_password = user_hashed.Password
                valid = bcrypt_sha256.verify(Password, hashed_password)
                return True
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
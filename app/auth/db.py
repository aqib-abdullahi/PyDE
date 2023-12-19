# from app.models.engine.mysql import MySQLDBstorage
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

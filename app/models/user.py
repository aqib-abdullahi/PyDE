"""User class"""
from app.models.base import Base
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean


class User(Base, UserMixin):
    """User model defined by various
    attributes
    Inherits from Base
    """
    __tablename__ = 'Users'

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    Email = Column(String(100))
    Password  = Column(String(100))
    Container = Column(String(150), nullable=True)
    Authenticated = Column(Boolean, default=False)

    def __init__(self, FirstName, LastName, Email, Password, Container, Authenticated):
        """Initializes the User class
        """
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Password = Password
        self.Container = Container
        self.Authenticated = Authenticated

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.Email
    
    def get_userid(self):
        """returns User ID """
        return self.UserID

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.Authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    def __repr__(self):
        """
        String rep.
        """
        return f"User: ID={self.UserID}"
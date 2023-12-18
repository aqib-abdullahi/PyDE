"""User class"""
from base import Base
from sqlalchemy import Column, Integer, String


class User(Base):
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
    Container = Column(String(150))

    def __init__(self, FirstName, LastName, Email, Password, Container):
        """Initializes the User class
        """
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.Password = Password
        self.Container = Container
    
    def __repr__(self):
        """
        String rep.
        """
        return f"User: ID={self.UserID}"
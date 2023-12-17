"""Defines the engine for MySQL database"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, joinedload
import os
from dotenv import load_dotenv
from app.models.base import Base


load_dotenv()
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
conn_string = f"mysql+mysqldb://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

class MySQLDBstorage:
    """defines the DBstorage class"""
    __session = None
    __engine = None

    def __init__(self):
        """initializes the database"""
        self.__engine = create_engine(conn_string,
                                      echo=True)

    def new(self, obj):
        """creates new  object to database"""
        MySQLDBstorage.__session.add(obj)

    def save(self):
        """saves or commit to database"""
        MySQLDBstorage.__session.commit()

    def delete(self, obj=None):
        """deletes from database"""
        MySQLDBstorage.__session.delete(obj)

    def reload(self):
        """reloads upon start"""
        # Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
        MySQLDBstorage.__session = self.__session

    def get_session(self):
        """Gets the session"""
        return self.__session

    def close(self):
        """closes  to release resources"""
        MySQLDBstorage.__session.close()
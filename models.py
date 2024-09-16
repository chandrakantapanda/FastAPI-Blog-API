from sqlalchemy import Boolean,Integer,String,Column
from database import Base #This is a common pattern when working with Object-Relational Mapping (ORM) libraries, particularly SQLAlchemy. The Base class is typically used as a declarative base class for defining database models. It provides a foundation for creating Python classes that represent tables in your database.
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250))
    email = Column(String(250), unique=True,index=True)

class Post(Base): 
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(250))
    user_id = Column(Integer)

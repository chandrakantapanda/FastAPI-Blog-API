from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


URL_DATABASE = 'mysql+pymysql://root:@localhost:3306/test'

engine = create_engine(URL_DATABASE)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
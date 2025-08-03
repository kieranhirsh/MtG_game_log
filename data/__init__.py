#!/usr/bin/python3
""" initialize the storage used by models """

from sqlalchemy.ext.declarative import declarative_base
from data.db_storage import DBStorage

Base = declarative_base()
storage = DBStorage(Base)

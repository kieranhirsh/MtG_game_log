#!/usr/bin/python3
""" initialize the storage used by models """

from data.db_storage import DBStorage
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
storage = DBStorage(Base)

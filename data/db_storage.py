#!/usr/bin/python3
""" This module defines a class to manage database storage """

import importlib
from os import getenv
from copy import deepcopy
from sqlalchemy import create_engine, text, and_, or_
from sqlalchemy.orm import scoped_session, sessionmaker

def build_query(node, classes):
    if "model" in node and "key" in node and "op" in node and "value" in node:
        model = node["model"]
        key = node["key"]
        op = node["op"]
        value = node["value"]
        if op == "==":
            class_ = classes[model]
            return getattr(class_, key) == value
        else:
            raise ValueError("Invalid operation: %s" % op)
    elif "clauses" in node and "op" in node:
        sub_clauses = [build_query(clause, classes) for clause in node["clauses"]]
        if node["op"] == "and":
            return(and_(*sub_clauses))
        elif node["op"] == "or":
            return(or_(*sub_clauses))
        else:
            raise ValueError("Invalid logical operation: %s" % op)
    else:
        raise ValueError("This node is lacking")

class DBStorage():
    """ Class for reading data from the database """
    __engine = None
    __session = None

    def __init__(self, Base):
        """Instantiate a DBStorage object"""

        # get environment variables
        user = getenv('MtG_log_MYSQL_USER')
        pwd = getenv('MtG_log_MYSQL_PWD')
        host = getenv('MtG_log_MYSQL_HOST')
        db = getenv('MtG_log_MYSQL_DB')

        # check that environment variables are set
        if user is None:
            raise TypeError("environment variable MtG_log_MYSQL_USER not set")
        if pwd is None:
            raise TypeError("environment variable MtG_log_MYSQL_PWD not set")
        if host is None:
            raise TypeError("environment variable MtG_log_MYSQL_HOST not set")
        if db is None:
            raise TypeError("environment variable MtG_log_MYSQL_DB not set")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db), pool_pre_ping=True)

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def get(self, class_name, join_classes=[], query_tree = {}, key = "", value = ""):
        """ Returns data for specified class name with or without record id"""
        if class_name.strip() == "":
            raise IndexError("Unable to load Model data. No class name specified")

        module = importlib.import_module("models." + class_name)
        class_ = getattr(module, class_name)

        if query_tree:
            classes = {class_name: class_}
            if join_classes:
                for join_name in join_classes:
                    join_module = importlib.import_module("models." + join_name)
                    join_class = getattr(join_module, join_name)
                    classes[join_name] = join_class
            where_clause = build_query(query_tree, classes)
            base_session = self.__session.query(class_)
            if join_classes:
                for join_name in join_classes:
                    join_module = importlib.import_module("models." + join_name)
                    join_class = getattr(join_module, join_name)
                    base_session = base_session.join(join_class)
            try:
                rows = base_session.where(where_clause).all()
            except:
                raise ValueError("Unable to load data from database.")
        else:
            if key != "" and value != "":
                try:
                    rows = self.__session.query(class_).where(getattr(class_, key) == value).all()
                except:
                    raise ValueError("Unable to load data from database.")
            elif key != "" and value == "":
                rows = []
            elif key == "" and value != "":
                raise ValueError("You have specified a value without a key, that makes no sense")
            else:
                rows = self.__session.query(class_).all()

        if not rows:
            raise IndexError("db_storage.get: no entry was found matching the given query.")

        return rows

    def add(self, new_record, do_commit = True):
        """ Adds another record to specified class """

        self.__session.add(new_record)

        if do_commit:
            self.__session.commit()
            self.__session.refresh(new_record)

    def add_all(self, new_records, do_commit = True):
        """ Adds and commits multiple records """

        self.__session.add_all(new_records)

        if do_commit:
            self.__session.commit()

    def update(self, class_name, record_id, update_data, allowed = None):
        """ Updates existing record of specified class """

        if class_name.strip() == "":
            raise IndexError("Unable to load Model data. No class name specified")

        module = importlib.import_module("models." + class_name)
        class_ = getattr(module, class_name)

        try:
            record = self.__session.query(class_).where(class_.id == record_id).limit(1).one()
        except:
            raise IndexError("Unable to find the record to update")

        try:
            for k, v in update_data.items():
                if allowed is not None and len(allowed) > 0:
                    if k in allowed:
                        setattr(record, k, v)
                    else:
                        print("Warning: %s property in %s class cannot be updated" % (k, class_name))
                else:
                    raise ValueError("No properties of the %s class can be updated" % (class_name))

            self.__session.commit()
        except:
            raise IndexError("Unable to update record")

        return deepcopy(record)

    def delete(self, class_name, record_id):
        """ Deletes specific record of specified class """

        if class_name.strip() == "":
            raise IndexError("Unable to load Model data. No class name specified")

        module = importlib.import_module("models." + class_name)
        class_ = getattr(module, class_name)

        try:
            data_to_del = self.__session.query(class_).where(class_.id == record_id).limit(1).one()
        except:
            raise IndexError("Unable to load Model data. Specified id not found")

        try:
            self.__session.delete(data_to_del)
            self.__session.commit()
        except:
            raise IndexError("Unable to delete record.")

    def contains(self, class_name, ids_list):
        """ Returns a simple TRUE or FALSE depending on whether all the ids in ids_list exist within the specified table """

        ids_count = len(ids_list)

        if ids_count == 0:
            raise IndexError("No record ids specified.")

        module = importlib.import_module("models." + class_name)
        class_ = getattr(module, class_name)

        rows = self.__session.query(class_).where(
            getattr(class_, 'id').in_(ids_list)
            ).all()

        return len(rows) == len(ids_list)

#!/usr/bin/python3
""" This module defines a class to manage database storage """

import importlib
from os import getenv
from copy import deepcopy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

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

    def get(self, class_name = "", key = "", value = ""):
        """ Returns data for specified class name with or without record id"""

        if class_name.strip() == "":
            raise IndexError("Unable to load Model data. No class name specified")

        module = importlib.import_module("models." + class_name)
        class_ = getattr(module, class_name)

        if key != "" and value != "":
            try:
                rows = self.__session.query(class_).where(getattr(class_, key) == value).all()
            except:
                raise IndexError("Unable to load Model data. Attribute " + key + " not found")
        elif key != "" and value == "":
            rows = []
        elif key == "" and value != "":
            raise ValueError("You have specified a value without a key, that makes no sense")
        else:
            rows = self.__session.query(class_).all()

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

    def raw_sql(self, query_txt, commit = False):
        """
            Accesses the database.
            Should I be using parametric queries? Yes
            Why aren't I? Because I know how to do it this way and the best code is the one you can write
        """
        sql = text(query_txt)
        result = self.__session.execute(sql)

        if commit == True:
            self.__session.commit()

        return result

    def conditions_to_raw_sql(self, conditions):
        """
            Converts a list of conditions to raw sql.
            Should I be using parametric queries? Yes
            Why aren't I? Because I know how to do it this way and the best code is the one you can write
        """
        query_text = "WHERE "
        i = 0

        for condition in conditions:
            if i > 0:
                query_text += " AND "
            if condition['not'] == True:
                query_text += "NOT "
            query_text += "%s." % condition['table']
            query_text += "%s " % condition['column']
            query_text += "%s " % condition['equality']
            query_text += "%s" % condition['value']
            i += 1

        query_text += ";"

        return query_text

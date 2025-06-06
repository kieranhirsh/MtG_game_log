#!/usr/bin/python
""" validation functions that are common to multiple models """
from data import storage

def valid_id(class_name, id):
    # check that the given id exists for the given class
    if not storage.get(class_name, id):
        raise ValueError("Invalid %s specified: %s" % (class_name, id))

    return True

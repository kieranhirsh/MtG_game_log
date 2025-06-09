#!/usr/bin/python
""" validation functions that are common to multiple models """
from data import storage

def valid_id(class_name, id):
    # check that the given id exists for the given class
    if not storage.get(class_name=class_name, key="id", value=id):
        raise ValueError("The desired %s could not be found" % (class_name))

    return True

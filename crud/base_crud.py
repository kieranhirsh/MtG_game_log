#!/usr/bin/python
""" CRUD layer """
from data import storage

class Base_crud():
    @staticmethod
    def get_parent_data(object_id, object_type, parent_type, return_model_object = False):
        """ Class method to get an object's the parent data """
        output = {}

        try:
            object_data = storage.get(class_name=object_type, key="id", value=object_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific colour identity\n"

        parent_id = getattr(object_data[0], "%s_id" % (parent_type.lower()))
        try:
            parent_data = storage.get(class_name=parent_type, key="id", value=parent_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific %s\n" % (parent_type)

        if return_model_object:
            return parent_data

        parent_columns = getattr(parent_data[0], "all_attribs")

        for column in parent_columns:
            output.update({column: getattr(parent_data[0], column)})

        return output

    @staticmethod
    def get_child_data(object_id, object_type, child_type, return_model_object = False):
        """ Class method get an object's child data """
        output = []

        try:
            child_data = storage.get(class_name=child_type, key="%s_id" % object_type, value=object_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific %s\n" % (child_type)

        if return_model_object:
            return child_data

        if child_data:
            child_columns = getattr(child_data[0], "all_attribs")

            i = 0
            for child in child_data:
                output.append({})

                for column in child_columns:
                    output[i].update({column: getattr(child, column)})

                i += 1

        return output


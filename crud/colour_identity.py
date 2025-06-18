#!/usr/bin/python
""" CRUD layer """
from flask import request, abort
from crud.base_crud import Base_crud
from data import storage
from models.colour_identity import Colour_Identity
from validation.colour_identity import Colour_Identity_validator

class Colour_Identity_crud():
    @staticmethod
    def all(return_model_object = False):
        """ Class method that returns all colour identities data """
        output = []

        try:
            result = storage.get(class_name = 'Colour_Identity')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load colour identities\n"

        if return_model_object:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "ci_name": row.ci_name,
                "colours": row.colours
            })

        return output

    @staticmethod
    def specific(key, value, return_model_object = False):
        """ Class method that returns a specific colour identity's data """
        try:
            result: Colour_Identity = storage.get(class_name = 'Colour_Identity', key = key, value = value)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load colour identity data\n"

        if return_model_object or not result:
            return result

        output = {
            "id": result[0].id,
            "ci_name": result[0].ci_name,
            "colours": result[0].colours
        }

        return output

    @staticmethod
    def create(data = "", return_model_object = False):
        """ Class method that creates a new colour identity """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        if 'ci_name' not in data:
            abort(400, "Missing ci_name")
        if 'colours' not in data:
            abort(400, "Missing colours")

        test_colour_identity = {
            "ci_name": data["ci_name"],
            "colours": data["colours"],
            "num_colours": data["num_colours"]
        }
        Colour_Identity_validator.is_valid(test_colour_identity)

        new_colour_identity = Colour_Identity(
            ci_name=data["ci_name"],
            colours=data["colours"],
            num_colours=data["num_colours"]
        )

        try:
            storage.add(new_colour_identity)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new colour_identity\n"

        if return_model_object:
            return new_colour_identity

        output = {
            "id": new_colour_identity.id,
            "ci_name": new_colour_identity.ci_name,
            "colours": new_colour_identity.colours
        }

        return output

    @staticmethod
    def update(colour_identity_id, data = "", return_model_object = False):
        """ Class method that updates an existing colour identity """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        colour_identity_to_update = Colour_Identity_crud.specific("id", colour_identity_id)
        for key in data:
            colour_identity_to_update[key] = data[key]

        Colour_Identity_validator.is_valid(colour_identity_to_update)

        try:
            result = storage.update('Colour_Identity', colour_identity_id, data, Colour_Identity.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified colour identity\n"

        if return_model_object:
            return result

        output = {
            "id": result.id,
            "ci_name": result.ci_name,
            "colours": result.colours
        }

        return output

    @staticmethod
    def delete(colour_identity_id):
        """ Class method that deletes an existing colour identity """
        try:
            # delete the colour identity record
            storage.delete('Colour_Identity', colour_identity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified colour identity\n"

        return Colour_Identity_crud.all()

    @staticmethod
    def get_parent_data(colour_identity_id, parent_type, return_model_object = False):
        """ Class method get the parent data for a given colour identity """
        output = {}

        try:
            colour_identity_data = storage.get(class_name="Colour_Identity", key="id", value=colour_identity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific colour identity\n"

        parent_id = getattr(colour_identity_data[0], "%s_id" % (parent_type.lower()))
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
    def get_sibling_data(colour_identity_id, parent_type, return_model_object = False):
        """ Class method get the sibling data for a given colour identity """
        output = []

        try:
            colour_identity_data = storage.get(class_name="Colour_Identity", key="id", value=colour_identity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific colour identity\n"

        parent_id = getattr(colour_identity_data[0], "%s_id" % (parent_type))
        try:
            sibling_data = storage.get(class_name="Colour_Identity", key="%s_id" % (parent_type), value=parent_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find sibling colour identities\n"

        if return_model_object:
            return sibling_data

        for sibling in sibling_data:
            output.append({
                "id": sibling.id,
                "ci_name": sibling.ci_name,
                "colours": sibling.colours
            })

        return output

    @staticmethod
    def get_child_data(colour_identity_id, child_type, return_model_object = False):
        return Base_crud.get_child_data(object_id=colour_identity_id,
                                        object_type="colour_identity",
                                        child_type=child_type,
                                        return_model_object=return_model_object)

#!/usr/bin/python
""" CRUD layer """
from flask import request, abort
from crud.base_crud import Base_crud
from data import storage
from models.colour_identity import colour_identity
from validation.colour_identity import colour_identity_validator

class colour_identity_crud():
    @staticmethod
    def all(return_model_object = False):
        """ Class method that returns all colour identities data """
        output = []

        try:
            result = storage.get(class_name = 'colour_identity')
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
            result = storage.get(class_name = 'colour_identity', key = key, value = value)
        except IndexError as exc:
            raise IndexError("Unable to load colour identity data")

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
        colour_identity_validator.is_valid(test_colour_identity)

        new_colour_identity = colour_identity(
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

        colour_identity_to_update = colour_identity_crud.specific("id", colour_identity_id)
        for key in data:
            colour_identity_to_update[key] = data[key]

        colour_identity_validator.is_valid(colour_identity_to_update)

        try:
            result = storage.update('colour_identity', colour_identity_id, data, colour_identity.can_update)
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
            storage.delete('colour_identity', colour_identity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified colour identity\n"

        return colour_identity_crud.all()

    @staticmethod
    def get_parent_data(colour_identity_id, parent_type, return_model_object = False):
        return Base_crud.get_parent_data(object_id=colour_identity_id,
                                         object_type="colour_identity",
                                         parent_type=parent_type,
                                         return_model_object=return_model_object)

    @staticmethod
    def get_sibling_data(colour_identity_id, parent_type, return_model_object = False):
        """ Class method get the sibling data for a given colour identity """
        output = []

        try:
            colour_identity_data = storage.get(class_name="colour_identity", key="id", value=colour_identity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific colour identity\n"

        parent_id = getattr(colour_identity_data[0], "%s_id" % (parent_type))
        try:
            sibling_data = storage.get(class_name="colour_identity", key="%s_id" % (parent_type), value=parent_id)
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

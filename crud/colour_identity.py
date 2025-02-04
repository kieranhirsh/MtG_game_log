#!/usr/bin/python
""" CRUD layer """
from flask import jsonify, request, abort
from data import storage
from models.colour_identity import Colour_Identity
from validation.colour_identity import Colour_Identity_validator

class Colour_Identity_crud():
    @staticmethod
    def all(return_raw_result = False):
        """ Class method that returns all colour identities data """
        output = []

        try:
            result = storage.get(class_name = 'Colour_Identity')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load colour identities\n"

        if return_raw_result:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "colour_identity": row.colour_identity,
                "colours": row.colours
            })

        return jsonify(output)

    @staticmethod
    def specific(colour_identity_id):
        """ Class method that returns a specific colour identity's data """
        try:
            result: Colour_Identity = storage.get(class_name = 'Colour_Identity', key = 'id', value = colour_identity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load colour identity data\n"

        output = {
            "id": result[0].id,
            "colour_identity": result[0].colour_identity,
            "colours": result[0].colours
        }

        return jsonify(output)

    @staticmethod
    def create(data = ""):
        """ Class method that creates a new colour identity """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        if 'name' not in data:
            abort(400, "Missing name")

        new_colour_identity = Colour_Identity(
            colour_identity=data["colour_identity"],
            colours=data["colours"]
        )
        is_valid = Colour_Identity_validator.is_valid(new_colour_identity)

        if is_valid:
            try:
                storage.add(new_colour_identity)
            except IndexError as exc:
                print("Error: ", exc)
                return "Unable to add new colour_identity\n"
        else:
            raise ValueError("Invalid colour_identity")

        output = {
            "id": new_colour_identity.id,
            "colour_identity": new_colour_identity.colour_identity,
            "olours": new_colour_identity.colours
        }

        return jsonify(output)

    @staticmethod
    def update(colour_identity_id, data = ""):
        """ Class method that updates an existing colour identity """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        # validate all possible inputs
        if 'colour_identity' in data:
            Colour_Identity_validator.valid_colour_identity(data["colour_identity"])
        if 'colours' in data:
            Colour_Identity_validator.valid_colours(data["colours"])

        try:
            result = storage.update('Colour_Identity', colour_identity_id, data, Colour_Identity.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified colour identity\n"

        output = {
            "id": result.id,
            "colour_identity": result.colour_identity,
            "colours": result.colours
        }

        return jsonify(output)

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
    def get_parent_data(colour_identity_id, parent_type):
        """ Class method get the parent data for a given colour identity """
        output = {}

        try:
            colour_identity_data = storage.get(class_name="Colour_Identity", key="id", value=colour_identity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific colour identity\n"

        parent_data = getattr(colour_identity_data[0], parent_type)
        parent_columns = getattr(parent_data, "all_attribs")

        for column in parent_columns:
            output.update({column: getattr(parent_data, column)})

        return jsonify(output)

    @staticmethod
    def get_sibling_data(colour_identity_id, parent_type):
        """ Class method get the sibling data for a given colour identity """
        output = []

        try:
            colour_identity_data = storage.get(class_name="Colour_Identity", key="id", value=colour_identity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific colour identity\n"

        parent_data = getattr(colour_identity_data[0], parent_type)
        sibling_data = getattr(parent_data, "colour_identities")

        for sibling in sibling_data:
            output.append({
                "id": sibling.id,
                "colour_identity": sibling.colour_identity,
                "colours": sibling.colours
            })

        return jsonify(output)

    @staticmethod
    def get_child_data(colour_identity_id, child_type):
        """ Class method get the child data for a given colour identity """
        output = []

        try:
            colour_identity_data = storage.get(class_name="Colour_Identity", key="id", value=colour_identity_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific colour identity\n"

        child_data = getattr(colour_identity_data[0], child_type)
        child_columns = getattr(child_data[0], "all_attribs")

        i = 0
        for child in child_data:
            output.append({})

            for column in child_columns:
                output[i].update({column: getattr(child, column)})

            i += 1

        return jsonify(output)

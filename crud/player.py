#!/usr/bin/python
""" CRUD layer """
from flask import jsonify, request, abort
from data import storage
from models.player import Player
from validation.player import Player_validator

class Player_crud():
    @staticmethod
    def all(return_raw_result = False):
        """ Class method that returns all players data """
        output = []

        try:
            result = storage.get(class_name = 'Player')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load players\n"

        if return_raw_result:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "name": row.name
            })

        return jsonify(output)

    @staticmethod
    def specific(player_id):
        """ Class method that returns a specific player's data """
        try:
            result: Player = storage.get(class_name = 'Player', key = 'id', value = player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Player data\n"

        output = {
            "id": result[0].id,
            "name": result[0].name
        }

        return jsonify(output)

    @staticmethod
    def create(data = ""):
        """ Class method that creates a new player """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        if 'name' not in data:
            abort(400, "Missing name")

        new_player = Player(
            name=data["name"]
        )
        is_valid = Player_validator.is_valid(new_player)

        if is_valid:
            try:
                storage.add(new_player)
            except IndexError as exc:
                print("Error: ", exc)
                return "Unable to add new Player\n"
        else:
            raise ValueError("Invalid player")

        output = {
            "id": new_player.id,
            "name": new_player.name
        }

        return jsonify(output)

    @staticmethod
    def update(player_id, data = ""):
        """ Class method that updates an existing player """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        # validate all possible inputs
        if 'name' in data:
            Player_validator.valid_name(data["name"])

        try:
            result = storage.update('Player', player_id, data, Player.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified player\n"

        output = {
            "id": result.id,
            "name": result.name
        }

        return jsonify(output)

    @staticmethod
    def delete(player_id):
        """ Class method that deletes an existing Player """
        try:
            # delete the Player record
            storage.delete('Player', player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified player\n"

        return Player_crud.all()

    @staticmethod
    def get_parent_data(player_id, parent_type):
        """ Class method get the parent data for a given Player """
        output = {}

        try:
            player_data = storage.get(class_name="Player", key="id", value=player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific player\n"

        parent_data = getattr(player_data[0], parent_type)
        parent_columns = getattr(parent_data, "all_attribs")

        for column in parent_columns:
            output.update({column: getattr(parent_data, column)})

        return jsonify(output)

    @staticmethod
    def get_sibling_data(player_id, parent_type):
        """ Class method get the sibling data for a given Player """
        output = []

        try:
            player_data = storage.get(class_name="Player", key="id", value=player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific player\n"

        parent_data = getattr(player_data[0], parent_type)
        sibling_data = getattr(parent_data, "players")

        for sibling in sibling_data:
            output.append({
                "id": sibling.id,
                "name": sibling.name
            })

        return jsonify(output)

    @staticmethod
    def get_child_data(player_id, child_type):
        """ Class method get the child data for a given Player """
        output = []

        try:
            player_data = storage.get(class_name="Player", key="id", value=player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific player\n"

        child_data = getattr(player_data[0], child_type)
        child_columns = getattr(child_data[0], "all_attribs")

        i = 0
        for child in child_data:
            output.append({})

            for column in child_columns:
                output[i].update({column: getattr(child, column)})

            i += 1

        return jsonify(output)

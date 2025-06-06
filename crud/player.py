#!/usr/bin/python
""" CRUD layer """
from flask import request, abort
from data import storage
from models.player import Player
from validation.player import Player_validator

class Player_crud():
    @staticmethod
    def all(return_model_object = False):
        """ Class method that returns all players data """
        output = []

        try:
            result = storage.get(class_name = 'Player')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load players\n"

        if return_model_object:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "player_name": row.player_name
            })

        return output

    @staticmethod
    def specific(key, value, return_model_object = False):
        """ Class method that returns a specific player's data """
        try:
            result: Player = storage.get(class_name = 'Player', key = key, value = value)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Player data\n"

        if return_model_object:
            return result

        output = {
            "id": result[0].id,
            "player_name": result[0].player_name
        }

        return output

    @staticmethod
    def create(data = "", return_model_object = False):
        """ Class method that creates a new player """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        if 'player_name' not in data:
            abort(400, "Missing player_name")

        test_player = {
            "player_name": data["player_name"]
        }
        Player_validator.is_valid(test_player)

        new_player = Player(
            player_name=data["player_name"]
        )

        try:
            storage.add(new_player)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Player\n"

        if return_model_object:
            return new_player

        output = {
            "id": new_player.id,
            "player_name": new_player.player_name
        }

        return output

    @staticmethod
    def update(player_id, data = "", return_model_object = False):
        """ Class method that updates an existing player """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        # validate all possible inputs
        test_player = {
            "player_name": data["player_name"]
        }
        Player_validator.is_valid(test_player)

        try:
            result = storage.update('Player', player_id, data, Player.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified player\n"

        if return_model_object:
            return result

        output = {
            "id": result.id,
            "player_name": result.player_name
        }

        return output

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
    def get_parent_data(player_id, parent_type, return_model_object = False):
        """ Class method get the parent data for a given Player """
        output = {}

        try:
            player_data = storage.get(class_name="Player", key="id", value=player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific player\n"

        parent_id = getattr(player_data[0], "%s_id" % (parent_type.lower()))
        try:
            parent_data = storage.get(class_name=parent_type, key="id", value=parent_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific %s\n" % (parent_type)

        if return_model_object:
            return parent_data

        parent_columns = getattr(parent_data, "all_attribs")

        for column in parent_columns:
            output.update({column: getattr(parent_data, column)})

        return output

    @staticmethod
    def get_sibling_data(player_id, parent_type, return_model_object = False):
        """ Class method get the sibling data for a given Player """
        output = []

        try:
            player_data = storage.get(class_name="Player", key="id", value=player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific player\n"

        parent_id = getattr(player_data[0], "%s_id" % (parent_type))
        try:
            sibling_data = storage.get(class_name="Player", key="%s_id" % (parent_type), value=parent_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find sibling players\n"

        if return_model_object:
            return sibling_data

        for sibling in sibling_data:
            output.append({
                "id": sibling.id,
                "player_name": sibling.player_name
            })

        return output

    @staticmethod
    def get_child_data(player_id, child_type, return_model_object = False):
        """ Class method get the child data for a given Player """
        output = []

        try:
            child_data = storage.get(class_name=child_type, key="player_id", value=player_id)
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

#!/usr/bin/python
""" CRUD layer """
from flask import request, abort
from crud.base_crud import Base_crud
from data import storage
from models.player import player
from validation.player import player_validator

class player_crud():
    @staticmethod
    def all(return_model_object = False):
        """ Class method that returns all players data """
        output = []

        try:
            result = storage.get(class_name = 'player')
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
            result: player = storage.get(class_name = 'player', key = key, value = value)
        except IndexError as exc:
            raise IndexError("Unable to load player data")

        if return_model_object or not result:
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
        player_validator.is_valid(test_player)

        new_player = player(
            player_name=data["player_name"]
        )

        try:
            storage.add(new_player)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new player\n"

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

        player_to_update = player_crud.specific("id", player_id)
        for key in data:
            player_to_update[key] = data[key]

        player_validator.is_valid(player_to_update)

        try:
            result = storage.update('player', player_id, data, player.can_update)
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
        """ Class method that deletes an existing player """
        try:
            # delete the player record
            storage.delete('player', player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified player\n"

        return player_crud.all()

    @staticmethod
    def get_parent_data(player_id, parent_type, return_model_object = False):
        return Base_crud.get_parent_data(object_id=player_id,
                                         object_type="player",
                                         parent_type=parent_type,
                                         return_model_object=return_model_object)

    @staticmethod
    def get_sibling_data(player_id, parent_type, return_model_object = False):
        """ Class method get the sibling data for a given player """
        output = []

        try:
            player_data = storage.get(class_name="player", key="id", value=player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific player\n"

        parent_id = getattr(player_data[0], "%s_id" % (parent_type))
        try:
            sibling_data = storage.get(class_name="player", key="%s_id" % (parent_type), value=parent_id)
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
        return Base_crud.get_child_data(object_id=player_id,
                                        object_type="player",
                                        child_type=child_type,
                                        return_model_object=return_model_object)

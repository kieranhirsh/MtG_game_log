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
            return "Unable to load players!"

        if return_raw_result:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "name": row.name,
            })

        return jsonify(output)

    @staticmethod
    def specific(player_id):
        """ Class method that returns a specific player's data """
        try:
            result: Player = storage.get(class_name = 'Player', key = 'id', value = player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Player data!"

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
                return "Unable to add new Player!"
        else:
            raise ValueError("Invalid player")

        output = {
            "id": new_player.id,
            "name": new_player.name
        }

        return jsonify(output)

    @staticmethod
    def update(player_id):
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
            return "Unable to update specified player!"

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
            return "Unable to delete specified player!"

        return Player.all()

    @staticmethod
    def get_decks_data(player_id):
        """ Class method get the data for a Player's decks """
        output = []

        try:
            player_data = storage.get(class_name="Player", key="id", value=player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific deck!"
        decks_data = player_data[0].decks

        for deck in decks_data:
            output.append({
                "id": deck.id,
                "commander": deck.commander
            })

        return jsonify(output)

#!/usr/bin/python
""" CRUD layer """
from flask import jsonify, request, abort
from data import storage
from models.deck import Deck
from validation.deck import Deck_validator

class Deck_crud():
    @staticmethod
    def all(return_raw_result = False):
        """ Class method that returns all decks data """
        output = []

        try:
            result = storage.get(class_name = 'Deck')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load decks!"

        if return_raw_result:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "commander": row.commander,
                "player_id": row.player_id
            })

        return jsonify(output)

    @staticmethod
    def specific(deck_id):
        """ Class method that returns a specific deck's data """
        try:
            result: Deck = storage.get(class_name = 'Deck', key = 'id', value = deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Deck data!"

        output = {
            "id": result[0].id,
            "commander": result[0].commander,
            "player_id": result[0].player_id
        }

        return jsonify(output)

    @staticmethod
    def create(data = ""):
        """ Class method that creates a new deck """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        if 'commander' not in data:
            abort(400, "Missing commander")
        if 'player_id' not in data:
            abort(400, "Missing player id")

        exists = storage.get(class_name = 'Player', key = 'id', value = data["player_id"])
        if exists is None:
            abort(400, "Specified player does not exist")

        new_deck = Deck(
            commander=data["commander"],
            player_id=data["player_id"]
        )
        is_valid = Deck_validator.is_valid(new_deck)

        if is_valid:
            try:
                storage.add(new_deck)
            except IndexError as exc:
                print("Error: ", exc)
                return "Unable to add new Deck!"
        else:
            raise ValueError("Invalid deck")

        output = {
            "id": new_deck.id,
            "commander": new_deck.commander,
            "player_id": new_deck.player_id
        }

        return jsonify(output)

    @staticmethod
    def update(deck_id, data = ""):
        """ Class method that updates an existing deck """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        # validate all possible inputs
        if 'commander' in data:
            Deck_validator.valid_commander(data["commander"])
        if 'player_id' in data:
            Deck_validator.valid_player_id(data["player_id"])

        try:
            result = storage.update('Deck', deck_id, data, Deck.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified deck!"

        output = {
            "id": result.id,
            "commander": result.commander,
            "player_id": result.player_id
        }

        return jsonify(output)

    @staticmethod
    def delete(deck_id):
        """ Class method that deletes an existing Deck """
        try:
            storage.delete('Deck', deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified deck!"

        return Deck.all()

    @staticmethod
    def get_parent_data(deck_id, class_type):
        """ Class method get the Parent data for a given Deck """
        output = {}

        try:
            deck_data = storage.get(class_name="Deck", key="id", value=deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific deck!"

        parent_data = getattr(deck_data[0], class_type)
        parent_columns = getattr(parent_data, "all_attribs")

        for column in parent_columns:
            output.update({column: getattr(parent_data, column)})

        return jsonify(output)

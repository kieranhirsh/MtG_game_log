#!/usr/bin/python
""" CRUD layer """
from flask import request, abort
from data import storage
from models.deck import Deck
from validation.deck import Deck_validator
######################## this needs to be fixed to match colour_identity
######################## more return_model_object are needed
######################## and checks to make sure getting children, siblings, and parents don't error when empty
######################## and make get child work correctly (probably fix parent and sibling layers too)
class Deck_crud():
    @staticmethod
    def all(return_model_object = False):
        """ Class method that returns all decks data """
        output = []

        try:
            result = storage.get(class_name = 'Deck')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load decks\n"

        if return_model_object:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "commander": row.commander,
                "player_id": row.player_id,
                "colour_identity_id": row.colour_identity_id
            })

        return output

    @staticmethod
    def specific(deck_id):
        """ Class method that returns a specific deck's data """
        try:
            result: Deck = storage.get(class_name = 'Deck', key = 'id', value = deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Deck data\n"

        output = {
            "id": result[0].id,
            "commander": result[0].commander,
            "player_id": result[0].player_id,
            "colour_identity_id": result[0].colour_identity_id
        }

        return output

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
        if 'colour_identity_id' not in data:
            abort(400, "Missing colour identity id")

        exists = storage.get(class_name = 'Player', key = 'id', value = data["player_id"])
        if exists is None:
            abort(400, "Specified player does not exist")
        exists = storage.get(class_name = 'Colour_Identity', key = 'id', value = data["colour_identity_id"])
        if exists is None:
            abort(400, "Specified colour identity does not exist")

        new_deck = Deck(
            commander=data["commander"],
            player_id=data["player_id"],
            colour_identity_id=data["colour_identity_id"]
        )
        is_valid = Deck_validator.is_valid(new_deck)

        if is_valid:
            try:
                storage.add(new_deck)
            except IndexError as exc:
                print("Error: ", exc)
                return "Unable to add new Deck\n"
        else:
            raise ValueError("Invalid deck")

        output = {
            "id": new_deck.id,
            "commander": new_deck.commander,
            "player_id": new_deck.player_id,
            "colour_identity_id": new_deck.colour_identity_id
        }

        return output

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
        if 'colour_identity_id' in data:
            Deck_validator.valid_player_id(data["colour_identity_id"])

        try:
            result = storage.update('Deck', deck_id, data, Deck.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified deck\n"

        output = {
            "id": result.id,
            "commander": result.commander,
            "player_id": result.player_id,
            "colour_identity_id": result.colour_identity_id
        }

        return output

    @staticmethod
    def delete(deck_id):
        """ Class method that deletes an existing Deck """
        try:
            storage.delete('Deck', deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified deck\n"

        return Deck_crud.all()

    @staticmethod
    def get_parent_data(deck_id, parent_type):
        """ Class method get the parent data for a given Deck """
        output = {}

        try:
            deck_data = storage.get(class_name="Deck", key="id", value=deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific deck\n"

        parent_data = getattr(deck_data[0], parent_type)
        parent_columns = getattr(parent_data, "all_attribs")

        for column in parent_columns:
            output.update({column: getattr(parent_data, column)})

        return output

    @staticmethod
    def get_sibling_data(deck_id, parent_type):
        """ Class method get the sibling data for a given Deck """
        output = []

        try:
            deck_data = storage.get(class_name="Deck", key="id", value=deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific deck\n"

        parent_data = getattr(deck_data[0], parent_type)
        sibling_data = getattr(parent_data, "decks")

        for sibling in sibling_data:
            output.append({
                "id": sibling.id,
                "commander": sibling.commander,
                "player_id": sibling.player_id,
                "colour_identity_id": sibling.colour_identity_id
            })

        return output

    @staticmethod
    def get_child_data(deck_id, child_type):
        """ Class method get the child data for a given Deck """
        output = []

        try:
            deck_data = storage.get(class_name="Deck", key="id", value=deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific deck\n"

        child_data = getattr(deck_data[0], child_type)
        child_columns = getattr(child_data[0], "all_attribs")

        i = 0
        for child in child_data:
            output.append({})

            for column in child_columns:
                output[i].update({column: getattr(child, column)})

            i += 1

        return output

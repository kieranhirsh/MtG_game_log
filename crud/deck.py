#!/usr/bin/python
""" CRUD layer """
from flask import request, abort
from data import storage
from models.deck import Deck
from validation.deck import Deck_validator

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
                "deck_name": row.deck_name,
                "player_id": row.player_id,
                "colour_identity_id": row.colour_identity_id
            })

        return output

    @staticmethod
    def specific(key, value, return_model_object = False):
        """ Class method that returns a specific deck's data """
        try:
            result: Deck = storage.get(class_name = 'Deck', key = key, value = value)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Deck data\n"

        if return_model_object:
            return result

        output = {
            "id": result[0].id,
            "deck_name": result[0].deck_name,
            "player_id": result[0].player_id,
            "colour_identity_id": result[0].colour_identity_id
        }

        return output

    @staticmethod
    def create(data = "", return_model_object = False):
        """ Class method that creates a new deck """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        if 'deck_name' not in data:
            abort(400, "Missing deck name")
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
            deck_name=data["deck_name"],
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

        if return_model_object:
            return new_deck

        output = {
            "id": new_deck.id,
            "deck_name": new_deck.deck_name,
            "player_id": new_deck.player_id,
            "colour_identity_id": new_deck.colour_identity_id
        }

        return output

    @staticmethod
    def update(deck_id, data = "", return_model_object = False):
        """ Class method that updates an existing deck """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        # validate all possible inputs
        if 'deck_name' in data:
            Deck_validator.valid_deck_name(data["deck_name"])
        if 'player_id' in data:
            Deck_validator.valid_player_id(data["player_id"])
        if 'colour_identity_id' in data:
            Deck_validator.valid_player_id(data["colour_identity_id"])

        try:
            result = storage.update('Deck', deck_id, data, Deck.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified deck\n"

        if return_model_object:
            return result

        output = {
            "id": result.id,
            "deck_name": result.deck_name,
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
    def get_parent_data(deck_id, parent_type, return_model_object = False):
        """ Class method get the parent data for a given Deck """
        output = {}

        try:
            deck_data = storage.get(class_name="Deck", key="id", value=deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific deck\n"

        parent_id = getattr(deck_data[0], "%s_id" % (parent_type.lower()))
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
    def get_sibling_data(deck_id, parent_type, return_model_object = False):
        """ Class method get the sibling data for a given Deck """
        output = []

        try:
            deck_data = storage.get(class_name="Deck", key="id", value=deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific deck\n"

        parent_id = getattr(deck_data[0], "%s_id" % (parent_type))
        try:
            sibling_data = storage.get(class_name="Deck", key="%s_id" % (parent_type), value=parent_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find sibling decks\n"

        if return_model_object:
            return sibling_data

        for sibling in sibling_data:
            output.append({
                "id": sibling.id,
                "deck_name": sibling.deck_name,
                "player_id": sibling.player_id,
                "colour_identity_id": sibling.colour_identity_id
            })

        return output

    @staticmethod
    def get_child_data(deck_id, child_type, return_model_object = False):
        """ Class method get the child data for a given Deck """
        output = []

        try:
            child_data = storage.get(class_name=child_type, key="deck_id", value=deck_id)
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

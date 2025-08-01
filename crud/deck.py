""" CRUD layer """
from flask import request, abort
from crud.base_crud import Base_crud
from data import storage
from models.deck import deck
from validation.deck import deck_validator

class deck_crud():
    @staticmethod
    def all(return_model_object = False):
        """ Class method that returns all decks data """
        output = []

        try:
            result = storage.get(class_name = 'deck')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load decks\n"

        if return_model_object:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "deck_name": row.deck_name,
                "commander_id": row.commander_id,
                "partner_id": row.partner_id,
                "companion_id": row.companion_id,
                "edhrec_num_decks": row.edhrec_num_decks,
                "edhrec_popularity": row.edhrec_popularity,
                "last_accessed": row.last_accessed,
                "player_id": row.player_id,
                "colour_identity_id": row.colour_identity_id
            })

        return output

    @staticmethod
    def specific(query_tree={}, join_classes=[], key="", value="", return_model_object=False):
        """ Class method that returns a specific deck's data """
        if query_tree:
            try:
                result = storage.get(class_name = 'deck', join_classes = join_classes, query_tree = query_tree)
            except IndexError as exc:
                raise IndexError("Unable to load deck data")
        else:
            try:
                result = storage.get(class_name = 'deck', key = key, value = value)
            except IndexError as exc:
                raise IndexError("Unable to load deck data")

        if return_model_object or not result:
            return result

        output = {
            "id": result[0].id,
            "deck_name": result[0].deck_name,
            "commander_id": result[0].commander_id,
            "partner_id": result[0].partner_id,
            "companion_id": result[0].companion_id,
            "edhrec_num_decks": result[0].edhrec_num_decks,
            "edhrec_popularity": result[0].edhrec_popularity,
            "last_accessed": result[0].last_accessed,
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

        test_deck = {
            "deck_name": data["deck_name"],
            "player_id": data["player_id"],
            "colour_identity_id": data["colour_identity_id"]
        }
        deck_validator.is_valid(test_deck)

        new_deck = deck(
            deck_name=data["deck_name"],
            commander_id=data["commander_id"],
            partner_id=data["partner_id"],
            companion_id=data["companion_id"],
            edhrec_num_decks=data["edhrec_num_decks"],
            edhrec_popularity=data["edhrec_popularity"],
            last_accessed=data["last_accessed"],
            player_id=data["player_id"],
            colour_identity_id=data["colour_identity_id"]
        )

        try:
            storage.add(new_deck)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new deck\n"

        if return_model_object:
            return new_deck

        output = {
            "id": new_deck.id,
            "deck_name": new_deck.deck_name,
            "commander_id": new_deck.commander_id,
            "partner_id": new_deck.partner_id,
            "companion_id": new_deck.companion_id,
            "edhrec_num_decks": new_deck.edhrec_num_decks,
            "edhrec_popularity": new_deck.edhrec_popularity,
            "last_accessed": new_deck.last_accessed,
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

        deck_to_update = deck_crud.specific(key="id", value=deck_id)
        for key in data:
            deck_to_update[key] = data[key]

        deck_validator.is_valid(deck_to_update)

        try:
            result = storage.update('deck', deck_id, data, deck.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified deck\n"

        if return_model_object:
            return result

        output = {
            "id": result.id,
            "deck_name": result.deck_name,
            "commander_id": result.commander_id,
            "partner_id": result.partner_id,
            "companion_id": result.companion_id,
            "edhrec_num_decks": result.edhrec_num_decks,
            "edhrec_popularity": result.edhrec_popularity,
            "last_accessed": result.last_accessed,
            "player_id": result.player_id,
            "colour_identity_id": result.colour_identity_id
        }

        return output

    @staticmethod
    def delete(deck_id):
        """ Class method that deletes an existing deck """
        try:
            storage.delete('deck', deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified deck\n"

        return deck_crud.all()

    @staticmethod
    def get_parent_data(deck_id, parent_type, return_model_object = False):
        return Base_crud.get_parent_data(object_id=deck_id,
                                         object_type="deck",
                                         parent_type=parent_type,
                                         return_model_object=return_model_object)

    @staticmethod
    def get_sibling_data(deck_id, parent_type, return_model_object = False):
        """ Class method get the sibling data for a given deck """
        output = []

        try:
            deck_data = storage.get(class_name="deck", key="id", value=deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific deck\n"

        parent_id = getattr(deck_data[0], "%s_id" % (parent_type))
        try:
            sibling_data = storage.get(class_name="deck", key="%s_id" % (parent_type), value=parent_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find sibling decks\n"

        if return_model_object:
            return sibling_data

        for sibling in sibling_data:
            output.append({
                "id": sibling.id,
                "deck_name": sibling.deck_name,
                "commander_id": sibling.commander_id,
                "partner_id": sibling.partner_id,
                "companion_id": sibling.companion_id,
                "edhrec_num_decks": sibling.edhrec_num_decks,
                "edhrec_popularity": sibling.edhrec_popularity,
                "last_accessed": sibling.last_accessed,
                "player_id": sibling.player_id,
                "colour_identity_id": sibling.colour_identity_id
            })

        return output

    @staticmethod
    def get_child_data(deck_id, child_type, return_model_object = False):
        return Base_crud.get_child_data(object_id=deck_id,
                                        object_type="deck",
                                        child_type=child_type,
                                        return_model_object=return_model_object)

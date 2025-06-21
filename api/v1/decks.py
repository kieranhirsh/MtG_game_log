""" objects that handles all default RestFul API actions for deck """
from flask import jsonify
from api.v1 import api_routes
from crud.deck import deck_crud

@api_routes.route('/decks', methods=["POST"])
def decks_post():
    """ posts data for new deck then returns the deck data """
    return jsonify(deck_crud.create())

@api_routes.route('/decks', methods=["GET"])
def decks_get():
    """ returns decks data """
    return jsonify(deck_crud.all())

@api_routes.route('/decks/<deck_id>', methods=["GET"])
def decks_get_specific(deck_id):
    """ returns specific deck data """
    return jsonify(deck_crud.specific('id', deck_id))

@api_routes.route('/decks/<deck_id>', methods=["PUT"])
def decks_edit(deck_id):
    """ updates existing deck data using specified id """
    return jsonify(deck_crud.update(deck_id))

@api_routes.route('/decks/<deck_id>/player', methods=["GET"])
def decks_get_player(deck_id):
    """ returns the data for a specific deck's owner """
    return jsonify(deck_crud.get_parent_data(deck_id, parent_type="player"))

@api_routes.route('/decks/<deck_id>/player_decks', methods=["GET"])
def decks_get_player_decks(deck_id):
    """ returns all the data for a specific deck's owner's decks """
    return jsonify(deck_crud.get_sibling_data(deck_id, parent_type="player"))

@api_routes.route('/decks/<deck_id>/colour_identity', methods=["GET"])
def decks_get_colour_identity(deck_id):
    """ returns the data for a specific deck's colour identity """
    return jsonify(deck_crud.get_parent_data(deck_id, parent_type="colour_identity"))

@api_routes.route('/decks/<deck_id>/colour_identity_decks', methods=["GET"])
def decks_get_colour_identity_decks(deck_id):
    """ returns the data for all deck's that share a specific deck's colour identity """
    return jsonify(deck_crud.get_sibling_data(deck_id, parent_type="colour_identity"))

@api_routes.route('/decks/<deck_id>', methods=["DELETE"])
def decks_delete(deck_id):
    """ deletes existing deck data using specified id """
    return jsonify(deck_crud.delete(deck_id))

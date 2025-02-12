""" objects that handles all default RestFul API actions for Player """
from flask import jsonify
from api.v1 import api_routes
from crud.player import Player_crud

@api_routes.route('/players', methods=["POST"])
def players_post():
    """ posts data for new player then returns the player data """
    return jsonify(Player_crud.create())

@api_routes.route('/players', methods=["GET"])
def players_get():
    """ returns players data """
    return jsonify(Player_crud.all())

@api_routes.route('/players/<player_id>', methods=["GET"])
def players_get_specific(player_id):
    """ returns specific player data """
    return jsonify(Player_crud.specific('id', player_id))

@api_routes.route('/players/<player_id>', methods=["PUT"])
def players_edit(player_id):
    """ updates existing player data using specified id """
    return jsonify(Player_crud.update(player_id))

@api_routes.route('/players/<player_id>/decks', methods=["GET"])
def players_get_decks(player_id):
    """ returns all of a specific player's decks' data """
    return jsonify(Player_crud.get_child_data(player_id, child_type="decks"))

@api_routes.route('/players/<player_id>', methods=["DELETE"])
def players_delete(player_id):
    """ deletes existing player data using specified id """
    return jsonify(Player_crud.delete(player_id))

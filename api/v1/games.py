""" objects that handles all default RestFul API actions for game """
from flask import jsonify
from api.v1 import api_routes
from crud.game import game_crud

@api_routes.route('/games', methods=["POST"])
def games_post():
    """ posts data for new game then returns the game data """
    return jsonify(game_crud.create())

@api_routes.route('/games', methods=["GET"])
def games_get():
    """ returns games data """
    return jsonify(game_crud.all())

@api_routes.route('/games/<game_id>', methods=["GET"])
def games_get_specific(game_id):
    """ returns specific game data """
    return jsonify(game_crud.specific('id', game_id))

@api_routes.route('/games/<game_id>', methods=["PUT"])
def games_edit(game_id):
    """ updates existing game data using specified id """
    return jsonify(game_crud.update(game_id))

@api_routes.route('/games/<game_id>/seats', methods=["GET"])
def games_get_seats(game_id):
    """ returns all of a specific game's seats' data """
    return jsonify(game_crud.get_child_data(game_id, child_type="Seat"))

@api_routes.route('/games/<game_id>', methods=["DELETE"])
def games_delete(game_id):
    """ deletes existing game data using specified id """
    return jsonify(game_crud.delete(game_id))

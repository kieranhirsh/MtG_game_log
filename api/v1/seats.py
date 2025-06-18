""" objects that handles all default RestFul API actions for Seat """
from flask import jsonify
from api.v1 import api_routes
from crud.seat import Seat_crud

@api_routes.route('/seats', methods=["POST"])
def seats_post():
    """ posts data for new seat then returns the seat data """
    return jsonify(Seat_crud.create())

@api_routes.route('/seats', methods=["GET"])
def seats_get():
    """ returns seats data """
    return jsonify(Seat_crud.all())

@api_routes.route('/seats/<seat_id>', methods=["GET"])
def seats_get_specific(seat_id):
    """ returns specific seat data """
    return jsonify(Seat_crud.specific('id', seat_id))

@api_routes.route('/seats/<seat_id>', methods=["PUT"])
def seats_edit(seat_id):
    """ updates existing seat data using specified id """
    return jsonify(Seat_crud.update(seat_id))

@api_routes.route('/seats/<seat_id>/player', methods=["GET"])
def seats_get_player(seat_id):
    """ returns the data for a specific seat's player """
    return jsonify(Seat_crud.get_parent_data(seat_id, parent_type="Player"))

@api_routes.route('/seats/<seat_id>/player_seats', methods=["GET"])
def seats_get_player_seats(seat_id):
    """ returns all the data for a specific seat's player's seats """
    return jsonify(Seat_crud.get_sibling_data(seat_id, parent_type="player"))

@api_routes.route('/seats/<seat_id>/deck', methods=["GET"])
def seats_get_deck(seat_id):
    """ returns the data for a specific seat's deck """
    return jsonify(Seat_crud.get_parent_data(seat_id, parent_type="Deck"))

@api_routes.route('/seats/<seat_id>/deck_seats', methods=["GET"])
def seats_get_deck_seats(seat_id):
    """ returns all the data for a specific seat's deck's seats """
    return jsonify(Seat_crud.get_sibling_data(seat_id, parent_type="deck"))

@api_routes.route('/seats/<seat_id>/game', methods=["GET"])
def seats_get_game(seat_id):
    """ returns the data for a specific seat's game """
    return jsonify(Seat_crud.get_parent_data(seat_id, parent_type="Game"))

@api_routes.route('/seats/<seat_id>/game_seats', methods=["GET"])
def seats_get_game_seats(seat_id):
    """ returns the data for all seat's in the given seat's game """
    return jsonify(Seat_crud.get_sibling_data(seat_id, parent_type="game"))

@api_routes.route('/seats/<seat_id>', methods=["DELETE"])
def seats_delete(seat_id):
    """ deletes existing seat data using specified id """
    return jsonify(Seat_crud.delete(seat_id))

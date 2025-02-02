""" objects that handles all default RestFul API actions for Player """
from api.v1 import api_routes
from models.player import Player

@api_routes.route('/players', methods=["POST"])
def players_post():
    """ posts data for new player then returns the player data """
    return Player.create()

@api_routes.route('/players', methods=["GET"])
def players_get():
    """ returns players data """
    return Player.all()

@api_routes.route('/players/<player_id>', methods=["GET"])
def players_specific_get(player_id):
    """ returns specific player data """
    return Player.specific(player_id)

@api_routes.route('/players/<player_id>', methods=["PUT"])
def players_edit(player_id):
    """ updates existing player data using specified id """
    return Player.update(player_id)

@api_routes.route('/players/<player_id>/decks', methods=["GET"])
def get_decks_data(player_id):
    """ returns all of a specific player's decks' data """
    return Player.get_decks_data(player_id)

@api_routes.route('/players/<player_id>', methods=["DELETE"])
def players_delete(player_id):
    """ deletes existing player data using specified id """
    return Player.delete(player_id)

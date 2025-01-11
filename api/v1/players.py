""" objects that handles all default RestFul API actions for Player """
from api.v1 import api_routes
from data import storage
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
def players_specific_decks_get(player_id):
    """ returns all of a specific player's decks' data """
    data = []

    player_data = storage.get(class_name="Player", key="id", value=player_id)
    print("======================================================================")
    print(player_data)
    print("======================================================================")
    decks_data = player_data[0].decks

    for deck in decks_data:
        data.append({
            "id": deck.id,
            "commander": deck.commander
        })

    return data

@api_routes.route('/players/<player_id>', methods=["DELETE"])
def players_delete(player_id):
    """ deletes existing player data using specified id """
    return Player.delete(player_id)

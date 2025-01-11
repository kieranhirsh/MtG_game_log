""" objects that handles all default RestFul API actions for Deck """
from api.v1 import api_routes
from models.deck import Deck

@api_routes.route('/decks', methods=["POST"])
def decks_post():
    """ posts data for new deck then returns the deck data """
    return Deck.create()

@api_routes.route('/decks', methods=["GET"])
def decks_get():
    """ returns decks data """
    return Deck.all()

@api_routes.route('/decks/<deck_id>', methods=["GET"])
def decks_specific_get(deck_id):
    """ returns specific deck data """
    return Deck.specific(deck_id)

@api_routes.route('/decks/<deck_id>', methods=["PUT"])
def decks_edit(deck_id):
    """ updates existing deck data using specified id """
    return Deck.update(deck_id)

@api_routes.route('/decks/<deck_id>/player', methods=["GET"])
def decks_specific_country_get(deck_id):
    """ returns the data for a specific deck's owner """
    data = []

    deck_data = Deck.specific(deck_id)
    player = deck_data[0].player

    data.append({
        "id": player.id,
        "commander": player.commander
    })

    return data

@api_routes.route('/decks/<deck_id>', methods=["DELETE"])
def decks_delete(deck_id):
    """ deletes existing deck data using specified id """
    return Deck.delete(deck_id)

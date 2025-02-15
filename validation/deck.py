#!/usr/bin/python
""" Deck validation """
import re
from data import storage

class Deck_validator():
    def is_valid(new_deck):
        # check all inputs are valid
        Deck_validator.valid_player_id(new_deck.player_id)
        Deck_validator.valid_deck_name(new_deck.deck_name)

        # if all checks are passed, we're good to go
        return True

    def valid_player_id(player_id):
        # ensure that the specified player id actually exists before setting
        if storage.get('Player', player_id) is None:
            raise ValueError("Invalid player_id specified: {}".format(player_id))

        return True

    def valid_deck_name(deck_name):
        # ensure that the deck name is not spaces-only and only contains allowed characters (alphabet, latin letters, and some punctuation)
        is_valid_deck_name = len(deck_name.strip()) > 0 and re.search("^[a-zA-Z\xC0-\xFF,' ()\"\!\?\\\/]*$", deck_name)
        if not is_valid_deck_name:
            raise ValueError("Invalid deck_name specified: {}".format(deck_name))

        return True

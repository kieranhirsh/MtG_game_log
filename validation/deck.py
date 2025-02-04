#!/usr/bin/python
""" Deck validation """
import re
from data import storage

class Deck_validator():
    def is_valid(new_deck):
        # check all inputs are valid
        Deck_validator.valid_player_id(new_deck.player_id)
        Deck_validator.valid_commander(new_deck.commander)

        # if all checks are passed, we're good to go
        return True

    def valid_player_id(player_id):
        # ensure that the specified player id actually exists before setting
        if storage.get('Player', player_id) is None:
            raise ValueError("Invalid player_id specified: {}".format(player_id))

        return True

    def valid_commander(commander):
        # ensure that the commander is not spaces-only and only contains allowed characters (alphabet, latin letters, and some punctuation)
        is_valid_commander = len(commander.strip()) > 0 and re.search("^[a-zA-Z\xC0-\xFF,' ]+$", commander)
        if not is_valid_commander:
            raise ValueError("Invalid commander specified: {}".format(commander))

        return True

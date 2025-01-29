#!/usr/bin/python
""" Deck validation """
import re
from data import storage

class Deck_validator():
    def is_valid(new_deck):
        # ensure that the commander is not spaces-only and only contains allowed characters (alphabet, latin letters, and some punctuation)
        is_valid_commander = len(new_deck.commander.strip()) > 0 and re.search("^[a-zA-Z\xC0-\xFF,' ]+$", new_deck.commander)
        if not is_valid_commander:
            raise ValueError("Invalid commander specified: {}".format(new_deck.commander))

        # ensure that the specified player id actually exists before setting
        if storage.get('Player', new_deck.player_id) is None:
            raise ValueError("Invalid player_id specified: {}".format(new_deck.player_id))

        # if all checks are passed, we're good to go
        return True

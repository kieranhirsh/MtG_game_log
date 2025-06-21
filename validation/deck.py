#!/usr/bin/python
""" deck validation """
import re
from validation import common

class deck_validator():
    def is_valid(new_deck):
        # check all inputs are valid
        deck_validator.valid_deck_name(new_deck["deck_name"])
        common.valid_id("Player", new_deck["player_id"])
        common.valid_id("colour_identity", new_deck["colour_identity_id"])

        # if all checks are passed, we're good to go
        return True

    def valid_deck_name(deck_name):
        # ensure that the deck name is not spaces-only and only contains allowed characters (alphabet, latin letters, and some punctuation)
        is_valid_deck_name = len(deck_name.strip()) > 0 and re.search("^[a-zA-ZÀ-ʯ,' ()\"\!\?\\\/\-&]*$", deck_name)
        if not is_valid_deck_name:
            raise ValueError("Invalid deck_name specified: {}".format(deck_name))

        return True

#!/usr/bin/python
""" Deck validation """
import re

class Player_validator():
    def is_valid(new_player):
        # check all inputs are valid
        Player_validator.valid_name(new_player.name)

        # if all checks are passed, we're good to go
        return True
    
    def valid_name(name):
        # ensure that the name is not spaces-only and only contains allowed characters (alphabet, latin letters, and some punctuation)
        is_valid_name = len(name.strip()) > 0 and re.search("^[a-zA-Z\xC0-\xFF,' ]+$", name)
        if not is_valid_name:
            raise ValueError("Invalid name specified: {}".format(name))

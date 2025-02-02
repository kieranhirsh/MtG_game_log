#!/usr/bin/python
""" Deck validation """
import re

class Player_validator():
    def is_valid(new_player):
        # ensure that the name is not spaces-only and only contains allowed characters (alphabet, latin letters, and some punctuation)
        is_valid_name = len(new_player.name.strip()) > 0 and re.search("^[a-zA-Z\xC0-\xFF,' ]+$", new_player.name)
        if not is_valid_name:
            raise ValueError("Invalid name specified: {}".format(new_player.name))

        # if all checks are passed, we're good to go
        return True

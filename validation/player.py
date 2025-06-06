#!/usr/bin/python
""" Player validation """
import re

class Player_validator():
    def is_valid(new_player):
        # check all inputs are valid
        Player_validator.valid_player_name(new_player["player_name"])

        # if all checks are passed, we're good to go
        return True

    def valid_player_name(player_name):
        # ensure that the name is not spaces-only and only contains allowed characters (alphabet, latin letters, and some punctuation)
        is_valid_name = len(player_name.strip()) > 0 and re.search("^[a-zA-ZÀ-ʯ,' \-]+$", player_name)
        if not is_valid_name:
            raise ValueError("Invalid name specified: {}".format(player_name))

        return True

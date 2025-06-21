#!/usr/bin/python
""" Seat validation """
from validation import common

class Seat_validator():
    def is_valid(new_seat):
        # check all inputs are valid
        Seat_validator.valid_seat_no(new_seat["seat_no"])
        Seat_validator.valid_ko_turn(new_seat["ko_turn"])
        common.valid_id("deck", new_seat["deck_id"])
        common.valid_id("Game", new_seat["game_id"])
        common.valid_id("player", new_seat["player_id"])

        # if all checks are passed, we're good to go
        return True

    def valid_seat_no(seat_no):
        # ensure that the specified seat number is an integer
        if seat_no % 1. != 0.:
            raise ValueError("Invalid seat_no specified: {}".format(seat_no))

        return True

    def valid_ko_turn(ko_turn):
        # ensure that the specified knock-out turn is an integer
        if (ko_turn is not None) and (ko_turn % 1. != 0.):
            raise ValueError("Invalid seat_no specified: {}".format(ko_turn))

        return True

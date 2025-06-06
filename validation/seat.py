#!/usr/bin/python
""" Seat validation """
from data import storage

class Seat_validator():
    def is_valid(new_seat):
        # check all inputs are valid
        Seat_validator.valid_seat_no(new_seat.seat_no)
        Seat_validator.valid_ko_turn(new_seat.ko_turn)
        Seat_validator.valid_deck_id(new_seat.deck_id)
        Seat_validator.valid_game_id(new_seat.game_id)
        Seat_validator.valid_player_id(new_seat.player_id)

        # if all checks are passed, we're good to go
        return True

    def valid_seat_no(seat_no):
        # ensure that the specified seat number is an integer
        if seat_no % 1. != 0.:
            raise ValueError("Invalid seat_no specified: {}".format(seat_no))

        return True

    def valid_ko_turn(ko_turn):
        # ensure that the specified knock-out turn is an integer
        if ko_turn % 1. != 0.:
            raise ValueError("Invalid seat_no specified: {}".format(ko_turn))

        return True

    def valid_deck_id(deck_id):
        # ensure that the specified deck id actually exists before setting
        if storage.get('Deck', deck_id) is None:
            raise ValueError("Invalid deck_id specified: {}".format(deck_id))

        return True

    def valid_game_id(game_id):
        # ensure that the specified game id actually exists before setting
        if storage.get('Game', game_id) is None:
            raise ValueError("Invalid game_id specified: {}".format(game_id))

        return True

    def valid_player_id(player_id):
        # ensure that the specified player id actually exists before setting
        if storage.get('Player', player_id) is None:
            raise ValueError("Invalid player_id specified: {}".format(player_id))

        return True

#!/usr/bin/python3

def game_length_in_time(game):
    if game.start_time and game.end_time:
        length_in_time = game.end_time - game.start_time
        time_seconds = length_in_time.seconds
        return str(length_in_time), time_seconds

    return None, None

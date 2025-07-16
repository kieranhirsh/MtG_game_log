#!/usr/bin/python3

def game_length_in_time(game):
    length_in_time = game.end_time - game.start_time
    time_seconds = length_in_time.seconds
    return str(length_in_time), time_seconds

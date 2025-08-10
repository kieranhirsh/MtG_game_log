''' utils that derive quantities from db data '''

def game_length_in_time(game):
    if game.start_time and game.end_time:
        length_in_time = game.end_time - game.start_time
        time_seconds = length_in_time.seconds
        return str(length_in_time), time_seconds

    return None, None

def game_length_in_turns(game):
    turns = 0
    for seat in game.seats:
        if seat.ko_turn and seat.ko_turn > turns:
            turns = seat.ko_turn

    return turns

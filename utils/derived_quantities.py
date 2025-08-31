''' utils that derive quantities from db data '''

def game_first_ko(game):
    first_ko_turn = 0
    for seat in game.seats:
        if seat.ko_turn and (not first_ko_turn or seat.ko_turn < first_ko_turn):
            first_ko_turn = seat.ko_turn

    if first_ko_turn:
        return first_ko_turn

    return None

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

    if turns:
        return turns

    return None

def game_winning_player_and_deck(game):
    '''
        This function takes a game object as an input, finds the winning seat,
        and outputs that seat's associated player object and game object.
        If the game didn't have exactly 1 winning seat it instead outputs "draw"
    '''
    winner = []
    for seat in game.seats:
        if not seat.ko_turn:
            winner.append([seat.player, seat.deck])

    if len(winner) != 1:
        # the game is a draw if there's not onee winner
        if len(winner) != len(game.seats):
            return "draw", "draw"
        else:
            # unless there is no ko turn data, in which case it's assumed that the data is missing
            return None, None

    return winner[0][0], winner[0][1]

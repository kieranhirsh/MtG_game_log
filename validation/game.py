#!/usr/bin/python
""" Game validation """
import re

class Game_validator():
    def is_valid(new_game):
        # check all inputs are valid
        Game_validator.valid_datetime(new_game.game_start_time)
        Game_validator.valid_datetime(new_game.game_end_time)

        # ensure that end time is after start time
        if new_game.game_start_time > new_game.game_end_time:
            raise ValueError("Invalid game start and end time specified (game must start before it ends): {} {}".format(new_game.game_start_time, new_game.game_end_time))

        # if all checks are passed, we're good to go
        return True

    def valid_datetime(datetime):
        # ensure that the time is in the format YYYY-MM-DD hh:mm:ss
        is_valid_datetime = re.search("^[1-9]([0-9]){3}-(0[0-9]|1[0-2])-([0-2][0-9]|3[0-1]) ([01][0-9]|2[0-3])(:[0-5][0-9]){2}$", datetime)
        if not is_valid_datetime:
            raise ValueError("Invalid datetime specified: {}".format(datetime))

        # yes, I am aware that this allows for Sep 31st, and I should have some logic here to prevent that
        # but leap years exist so I'm not opening that rabbit hole

        return True

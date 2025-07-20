""" game validation """
import datetime
import re

class game_validator():
    def is_valid(new_game):
        # check all inputs are valid
        game_validator.valid_time(new_game["start_time"])
        game_validator.valid_time(new_game["end_time"])

        # ensure that end time is after start time
        if str(new_game["start_time"]) > str(new_game["end_time"]):
            raise ValueError("Invalid game start and end time specified (game must start before it ends): {} {}".format(new_game["start_time"], new_game["end_time"]))

        # if all checks are passed, we're good to go
        return True

    def valid_time(time):
        # ensure that the time is of type str or datetime.datetime
        if not type(time) == str and not type(time) == datetime.datetime:
            raise TypeError("Invalid datetime type: {}".format(type(time)))

        # ensure that the time is in the format YYYY-MM-DD hh:mm:ss
        # YYYY-MM-DD: required
        # hh:mm:ss: optional (hh and hh:mm also accepted)
        is_valid_datetime = re.search("^[1-9]([0-9]){3}-(0[0-9]|1[0-2])-([0-2][0-9]|3[0-1])( ([01][0-9]|2[0-3])(:[0-5][0-9]){0,2}){0,1}$", str(time))
        # yes, I am aware that this allows for Sep 31st, and I should have some logic here to prevent that
        # but leap years exist so I'm not opening that rabbit hole
        if not is_valid_datetime:
            raise ValueError("Invalid datetime specified: {}".format(time))

        return True

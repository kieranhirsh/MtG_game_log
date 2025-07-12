#!/usr/bin/python
""" CRUD layer """
from flask import request, jsonify
from crud.base_crud import Base_crud
from data import storage
from models.game import game
from validation.game import game_validator

month_dict = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December"
}

class game_crud():
    @staticmethod
    def all(return_model_object = False):
        """ Class method that returns all games data """
        output = []

        try:
            result = storage.get(class_name = 'game')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load games\n"

        if return_model_object:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "game_name": row.game_name,
                "month": row.month,
                "year": row.year,
                "start_time": row.start_time,
                "end_time": row.end_time,
                "game_time": row.game_time,
                "game_turns": row.game_turns,
                "winning_deck_id": row.winning_deck_id,
                "winning_player_id": row.winning_player_id
            })

        return output

    @staticmethod
    def specific(key, value, return_model_object = False):
        """ Class method that returns a specific game's data """
        try:
            result = storage.get(class_name = 'game', key = key, value = value)
        except IndexError as exc:
            raise IndexError("Unable to load game data")

        if not result:
            raise IndexError("No game found")

        if return_model_object:
            return result

        output = {
            "id": result[0].id,
            "game_name": result[0].game_name,
            "month": result[0].month,
            "year": result[0].year,
            "start_time": result[0].start_time,
            "end_time": result[0].end_time,
            "game_time": result[0].game_time,
            "game_turns": result[0].game_turns,
            "winning_deck_id": result[0].winning_deck_id,
            "winning_player_id": result[0].winning_player_id
        }

        return output

    @staticmethod
    def create(data = "", return_model_object = False):
        """ Class method that creates a new game """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        test_game = {}
        for field in game.can_init:
            test_game[field] = ""
        for key in data:
            test_game[key] = data[key]

        month_num = data["start_time"][5:7]
        test_game["month"] = month_dict[month_num]
        year = int(data["start_time"][0:4])
        test_game["year"] = year
        game_validator.is_valid(test_game)

        new_game = game(
            game_name=test_game["game_name"],
            month=month_dict[month_num],
            year=year,
            start_time=test_game["start_time"],
            end_time=test_game["end_time"],
            game_time=test_game["game_time"],
            game_turns=None,
            winning_deck_id=None,
            winning_player_id=None
        )

        try:
            storage.add(new_game)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new game\n"

        if return_model_object:
            return new_game

        output = {
            "id": new_game.id,
            "game_name": new_game.game_name,
            "month": new_game.month,
            "year": new_game.year,
            "start_time": new_game.start_time,
            "end_time": new_game.end_time,
            "game_time": new_game.game_time,
            "game_turns": new_game.game_turns,
            "winning_deck_id": new_game.winning_deck_id,
            "winning_player_id": new_game.winning_player_id
        }

        return output

    @staticmethod
    def update(game_id, data = "", return_model_object = False):
        """ Class method that updates an existing game """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        call_validator = False
        game_to_update = game_crud.specific("id", game_id)
        for key in data:
            game_to_update[key] = data[key]
            if key == "start_time" or key == "end_time":
                call_validator = True

        if "start_time" in data:
            month_num = data["start_time"][5:7]
            game_to_update["month"] = month_dict[month_num]
            data["month"] = month_dict[month_num]
            year = int(data["start_time"][0:4])
            game_to_update["year"] = year
            data["year"] = year

        if call_validator:
            game_validator.is_valid(game_to_update)

        try:
            result = storage.update('game', game_id, data, game.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified game\n"

        if return_model_object:
            return result

        output = {
            "id": result.id,
            "game_name": result.game_name,
            "month": result.month,
            "year": result.year,
            "start_time": result.start_time,
            "end_time": result.end_time,
            "game_time": result.game_time,
            "game_turns": result.game_turns,
            "winning_deck_id": result.winning_deck_id,
            "winning_player_id": result.winning_player_id
        }

        return output

    @staticmethod
    def update_game_name(game_id, return_model_object = False):
        # find the game entry to be updated
        game_object = game_crud.specific("id", game_id, True)

        # get the data we need to generate the name
        start_time = str(game_object[0].start_time)
        end_time = str(game_object[0].end_time)

        # generate the name
        game_name = start_time[:-3] + " - " + end_time[-8:-3]

        # create an updated game dict
        updated_game = {
            "game_name": game_name
        }

        # update the game entry
        return game_crud.update(game_id=game_id, data=jsonify(updated_game), return_model_object=return_model_object)

    @staticmethod
    def update_game_time(game_id, return_model_object = False):
        # find the game entry to be updated
        game_object = game_crud.specific("id", game_id, True)

        # get the data we need to generate the name
        start_time = game_object[0].start_time
        end_time = game_object[0].end_time

        # generate the name
        game_time = str(end_time - start_time)

        # create an updated game dict
        updated_game = {
            "game_time": game_time
        }

        # update the game entry
        return game_crud.update(game_id=game_id, data=jsonify(updated_game), return_model_object=return_model_object)

    @staticmethod
    def update_game_turns(game_id, return_model_object = False):
        # find the game entry to be updated
        game_object = game_crud.specific("id", game_id, True)

        # get the data we need to generate the name
        seats = game_crud.get_child_data(game_object[0].id, "seat", True)

        # calculate the game length in turns
        game_turns = 0
        for seat in seats:
            if seat.ko_turn and seat.ko_turn > game_turns:
                game_turns = seat.ko_turn

        # create an updated game dict
        updated_game = {
            "game_turns": game_turns
        }

        # update the game entry
        return game_crud.update(game_id=game_id, data=jsonify(updated_game), return_model_object=return_model_object)

    @staticmethod
    def update_game_winner(game_id, return_model_object = False):
        # find the game entry to be updated
        game_object = game_crud.specific("id", game_id, True)

        seats = game_crud.get_child_data(game_object[0].id, "seat", True)

        for seat in seats:
            if seat.ko_turn is None:
                updated_game = {
                    "winning_deck_id": seat.deck_id,
                    "winning_player_id": seat.player_id
                }

        # update the game entry
        return game_crud.update(game_id=game_id, data=jsonify(updated_game), return_model_object=return_model_object)

    @staticmethod
    def delete(game_id):
        """ Class method that deletes an existing game """
        try:
            # delete the game record
            storage.delete('game', game_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified game\n"

        return game_crud.all()

    @staticmethod
    def get_parent_data(game_id, parent_type, return_model_object = False):
        return Base_crud.get_parent_data(object_id=game_id,
                                         object_type="game",
                                         parent_type=parent_type,
                                         return_model_object=return_model_object)

    @staticmethod
    def get_sibling_data(game_id, parent_type, return_model_object = False):
        """ Class method get the sibling data for a given game """
        output = []

        try:
            game_data = storage.get(class_name="game", key="id", value=game_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific game\n"

        parent_id = getattr(game_data[0], "%s_id" % (parent_type))
        try:
            sibling_data = storage.get(class_name="game", key="%s_id" % (parent_type), value=parent_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find sibling games\n"

        if return_model_object:
            return sibling_data

        for sibling in sibling_data:
            output.append({
                "id": sibling.id,
                "game_name": sibling.game_name,
                "start_time": sibling.start_time,
                "end_time": sibling.end_time,
                "game_time": sibling.game_time
            })

        return output

    @staticmethod
    def get_child_data(game_id, child_type, return_model_object = False):
        return Base_crud.get_child_data(object_id=game_id,
                                        object_type="game",
                                        child_type=child_type,
                                        return_model_object=return_model_object)

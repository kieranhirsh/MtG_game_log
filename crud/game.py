#!/usr/bin/python
""" CRUD layer """
from flask import request, jsonify
from data import storage
from models.game import Game
from validation.game import Game_validator

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

class Game_crud():
    @staticmethod
    def all(return_model_object = False):
        """ Class method that returns all games data """
        output = []

        try:
            result = storage.get(class_name = 'Game')
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
                "winning_deck_id": row.winning_deck_id,
                "winning_player_id": row.winning_player_id
            })

        return output

    @staticmethod
    def specific(key, value, return_model_object = False):
        """ Class method that returns a specific game's data """
        try:
            result: Game = storage.get(class_name = 'Game', key = key, value = value)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Game data\n"

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
        for field in Game.can_init:
            test_game[field] = ""
        for key in data:
            test_game[key] = data[key]

        month_num = data["start_time"][5:7]
        test_game["month"] = month_dict[month_num]
        year = int(data["start_time"][0:4])
        test_game["year"] = year
        Game_validator.is_valid(test_game)

        new_game = Game(
            game_name=test_game["game_name"],
            month=month_dict[month_num],
            year=year,
            start_time=test_game["start_time"],
            end_time=test_game["end_time"],
            game_time=test_game["game_time"],
            winning_deck_id=None,
            winning_player_id=None
        )

        try:
            storage.add(new_game)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Game\n"

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
        game_to_update = Game_crud.specific("id", game_id)
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
            Game_validator.is_valid(game_to_update)

        try:
            result = storage.update('Game', game_id, data, Game.can_update)
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
            "winning_deck_id": result.winning_deck_id,
            "winning_player_id": result.winning_player_id
        }

        return output

    @staticmethod
    def update_game_name(game_id, return_model_object = False):
        # find the game entry to be updated
        game_object = Game_crud.specific("id", game_id, True)

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
        return Game_crud.update(game_id=game_id, data=jsonify(updated_game), return_model_object=return_model_object)

    @staticmethod
    def update_game_time(game_id, return_model_object = False):
        # find the game entry to be updated
        game_object = Game_crud.specific("id", game_id, True)

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
        return Game_crud.update(game_id=game_id, data=jsonify(updated_game), return_model_object=return_model_object)

    @staticmethod
    def update_game_winner(game_id, return_model_object = False):
        # find the game entry to be updated
        game_object = Game_crud.specific("id", game_id, True)

        seats = Game_crud.get_child_data(game_object[0].id, "Seat", True)

        for seat in seats:
            print(seat.ko_turn)
            if seat.ko_turn is None:
                updated_game = {
                    "winning_deck_id": seat.deck_id,
                    "winning_player_id": seat.player_id
                }
                print(updated_game)

        # update the game entry
        return Game_crud.update(game_id=game_id, data=jsonify(updated_game), return_model_object=return_model_object)

    @staticmethod
    def delete(game_id):
        """ Class method that deletes an existing Game """
        try:
            # delete the Game record
            storage.delete('Game', game_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified game\n"

        return Game_crud.all()

    @staticmethod
    def get_parent_data(game_id, parent_type, return_model_object = False):
        """ Class method get the parent data for a given Game """
        output = {}

        try:
            game_data = storage.get(class_name="Game", key="id", value=game_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific game\n"

        parent_id = getattr(game_data[0], "%s_id" % (parent_type.lower()))
        try:
            parent_data = storage.get(class_name=parent_type, key="id", value=parent_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific %s\n" % (parent_type)

        if return_model_object:
            return parent_data

        parent_columns = getattr(parent_data, "all_attribs")

        for column in parent_columns:
            output.update({column: getattr(parent_data, column)})

        return output

    @staticmethod
    def get_sibling_data(game_id, parent_type, return_model_object = False):
        """ Class method get the sibling data for a given Game """
        output = []

        try:
            game_data = storage.get(class_name="Game", key="id", value=game_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific game\n"

        parent_id = getattr(game_data[0], "%s_id" % (parent_type))
        try:
            sibling_data = storage.get(class_name="Game", key="%s_id" % (parent_type), value=parent_id)
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
        """ Class method get the child data for a given Game """
        output = []

        try:
            child_data = storage.get(class_name=child_type, key="game_id", value=game_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific %s\n" % (child_type)

        if return_model_object:
            return child_data

        if child_data:
            child_columns = getattr(child_data[0], "all_attribs")

            i = 0
            for child in child_data:
                output.append({})

                for column in child_columns:
                    output[i].update({column: getattr(child, column)})

                i += 1

        return output

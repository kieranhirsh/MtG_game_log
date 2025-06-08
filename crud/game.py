#!/usr/bin/python
""" CRUD layer """
from flask import request
from data import storage
from models.game import Game
from validation.game import Game_validator

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
                "start_time": row.start_time,
                "end_time": row.end_time
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
            "start_time": result[0].start_time,
            "end_time": result[0].end_time
        }

        return output

    @staticmethod
    def create(data = "", return_model_object = False):
        """ Class method that creates a new game """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        test_game = {
            "start_time": data["start_time"],
            "end_time": data["end_time"]
        }
        Game_validator.is_valid(test_game)

        new_game = Game(
            start_time=data["start_time"],
            end_time=data["end_time"]
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
            "start_time": new_game.start_time,
            "end_time": new_game.end_time
        }

        return output

    @staticmethod
    def update(game_id, data = "", return_model_object = False):
        """ Class method that updates an existing game """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        # validate all possible inputs
        test_game = {
            "start_time": data["start_time"],
            "end_time": data["end_time"]
        }
        Game_validator.is_valid(test_game)

        try:
            result = storage.update('Game', game_id, data, Game.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified game\n"

        if return_model_object:
            return result

        output = {
            "id": result.id,
            "start_time": result.start_time,
            "end_time": result.end_time
        }

        return output

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
                "start_time": sibling.start_time,
                "end_time": sibling.end_time
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

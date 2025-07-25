""" CRUD layer """
from flask import request, abort
from crud.base_crud import Base_crud
from data import storage
from models.seat import seat
from validation.seat import seat_validator

class seat_crud():
    @staticmethod
    def all(return_model_object = False):
        """ Class method that returns all seats data """
        output = []

        try:
            result = storage.get(class_name = 'seat')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load seats\n"

        if return_model_object:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "seat_no": row.seat_no,
                "ko_turn": row.ko_turn,
                "deck_id": row.deck_id,
                "game_id": row.game_id,
                "player_id": row.player_id
            })

        return output

    @staticmethod
    def specific(key, value, return_model_object = False):
        """ Class method that returns a specific seat's data """
        try:
            results: seat = storage.get(class_name = 'seat', key = key, value = value)
        except IndexError as exc:
            raise IndexError("Unable to load seat data")

        if return_model_object or not results:
            return results

        output = []
        for result in results:
            output.append(
                {
                    "id": result.id,
                    "seat_no": result.seat_no,
                    "ko_turn": result.ko_turn,
                    "deck_id": result.deck_id,
                    "game_id": result.game_id,
                    "player_id": result.player_id
                }
            )

        return output

    @staticmethod
    def create(data = "", return_model_object = False):
        """ Class method that creates a new seat """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        if 'seat_no' not in data:
            abort(400, "Missing seat number")
        if 'ko_turn' not in data:
            abort(400, "Missing ko turn")
        if 'deck_id' not in data:
            abort(400, "Missing deck id")
        if 'game_id' not in data:
            abort(400, "Missing game id")
        if 'player_id' not in data:
            abort(400, "Missing player id")

        test_seat = {
            "seat_no": data["seat_no"],
            "ko_turn": data["ko_turn"],
            "deck_id": data["deck_id"],
            "game_id": data["game_id"],
            "player_id": data["player_id"]
        }
        seat_validator.is_valid(test_seat)

        new_seat = seat(
            seat_no=data["seat_no"],
            ko_turn=data["ko_turn"],
            deck_id=data["deck_id"],
            game_id=data["game_id"],
            player_id=data["player_id"]
        )

        try:
            storage.add(new_seat)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new seat\n"

        if return_model_object:
            return new_seat

        output = {
            "id": new_seat.id,
            "seat_no": new_seat.seat_no,
            "ko_turn": new_seat.ko_turn,
            "deck_id": new_seat.deck_id,
            "game_id": new_seat.game_id,
            "player_id": new_seat.player_id
        }

        return output

    @staticmethod
    def update(seat_id, data = "", return_model_object = False):
        """ Class method that updates an existing seat """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        seat_to_update = seat_crud.specific("id", seat_id)[0]
        for key in data:
            seat_to_update[key] = data[key]

        seat_validator.is_valid(seat_to_update)

        try:
            result = storage.update('seat', seat_id, data, seat.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified seat\n"

        if return_model_object:
            return result

        output = {
            "id": result.id,
            "seat_no": result.seat_no,
            "ko_turn": result.ko_turn,
            "deck_id": result.deck_id,
            "game_id": result.game_id,
            "player_id": result.player_id
        }

        return output

    @staticmethod
    def delete(seat_id):
        """ Class method that deletes an existing seat """
        try:
            storage.delete('seat', seat_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified seat\n"

        return seat_crud.all()

    @staticmethod
    def get_parent_data(seat_id, parent_type, return_model_object = False):
        return Base_crud.get_parent_data(object_id=seat_id,
                                         object_type="seat",
                                         parent_type=parent_type,
                                         return_model_object=return_model_object)

    @staticmethod
    def get_sibling_data(seat_id, parent_type, return_model_object = False):
        """ Class method get the sibling data for a given seat """
        output = []

        try:
            seat_data = storage.get(class_name="seat", key="id", value=seat_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find specific decseatk\n"

        parent_id = getattr(seat_data[0], "%s_id" % (parent_type))
        try:
            sibling_data = storage.get(class_name="seat", key="%s_id" % (parent_type), value=parent_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to find sibling seats\n"

        if return_model_object:
            return sibling_data

        for sibling in sibling_data:
            output.append({
            "id": sibling.id,
            "seat_no": sibling.seat_no,
            "ko_turn": sibling.ko_turn,
            "deck_id": sibling.deck_id,
            "game_id": sibling.game_id,
            "player_id": sibling.player_id
            })

        return output

    @staticmethod
    def get_child_data(seat_id, child_type, return_model_object = False):
        return Base_crud.get_child_data(object_id=seat_id,
                                        object_type="seat",
                                        child_type=child_type,
                                        return_model_object=return_model_object)

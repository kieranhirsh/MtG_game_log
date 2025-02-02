#!/usr/bin/python
""" Deck model """
import uuid
from flask import jsonify, request, abort
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from data import storage, Base
from validation.deck import Deck_validator

class Deck(Base):
    """ Representation of deck """

    can_init   = ["commander", "player_id"]
    can_update = ["commander", "player_id"]

    # Class attributes defaults
    __tablename__ = 'Decks'
    id        = Column(String(64), nullable=False, primary_key=True)
    commander = Column("commander", String(128), nullable=False)
    player_id = Column("player_id", String(128), ForeignKey('Players.id'), nullable=False)
    player    = relationship("Player", back_populates="decks")

    # constructor
    def __init__(self, *args, **kwargs):
        """ constructor """
        # Set object instance defaults
        self.id = str(uuid.uuid4())

        # Note that setattr will call the setters for attribs in the list
        if kwargs:
            for key, value in kwargs.items():
                if key in self.can_init:
                    setattr(self, key, value)


    # --- Static methods ---
    @staticmethod
    def all(return_raw_result = False):
        """ Class method that returns all decks data """
        output = []

        try:
            result = storage.get(class_name = 'Deck')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load decks!"

        if return_raw_result:
            return result

        for row in result:
            output.append({
                "id": row.id,
                "commander": row.commander,
                "player_id": row.player_id
            })

        return jsonify(output)

    @staticmethod
    def specific(deck_id):
        """ Class method that returns a specific deck's data """
        try:
            result: Deck = storage.get(class_name = 'Deck', key = 'id', value = deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Deck data!"

        output = {
            "id": result[0].id,
            "commander": result[0].commander,
            "player_id": result[0].player_id
        }

        return jsonify(output)

    @staticmethod
    def create(data = ""):
        """ Class method that creates a new deck """
        try:
            data = request.get_json()
        except:
            data = data.get_json()

        if 'commander' not in data:
            abort(400, "Missing commander")
        if 'player_id' not in data:
            abort(400, "Missing player id")

        exists = storage.get(class_name = 'Player', key = 'id', value = data["player_id"])
        if exists is None:
            abort(400, "Specified player does not exist")

        new_deck = Deck(
            commander=data["commander"],
            player_id=data["player_id"]
        )
        is_valid = Deck_validator.is_valid(new_deck)

        if is_valid:
            try:
                storage.add(new_deck)
            except IndexError as exc:
                print("Error: ", exc)
                return "Unable to add new Deck!"
        else:
            raise ValueError("Invalid deck")

        output = {
            "id": new_deck.id,
            "commander": new_deck.commander,
            "player_id": new_deck.player_id
        }

        return jsonify(output)

    @staticmethod
    def update(deck_id):
        ############# THIS IS SUPER OUTDATED #############
        """ Class method that updates an existing deck """
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        try:
            # update the Deck record. Only commander can be changed
            result = storage.update('Deck', deck_id, data, Deck.can_update)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified deck!"

        output = {
            "id": result.id,
            "commander": result.commander,
            "player_id": result.player_id
        }

        return jsonify(output)

    @staticmethod
    def delete(deck_id):
        """ Class method that deletes an existing Deck """
        try:
            # delete the Deck record
            storage.delete('Deck', deck_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified deck!"

        return Deck.all()

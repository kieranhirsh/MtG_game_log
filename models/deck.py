#!/usr/bin/python
""" Deck model """

import uuid
import re
from flask import jsonify, request, abort
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from data import storage, Base

class Deck(Base):
    """ Representation of deck """

    can_init   = ["commander", "player_id"]
    can_update = ["commander", "player_id"]

    # Class attributes defaults
    __tablename__ = 'decks'
    id          = Column(String(64), nullable=False, primary_key=True)
    __commander = Column("commander", String(128), nullable=False)
    __player_id = Column("player_id", String(128), ForeignKey('players.id'), nullable=False)
    player      = relationship("Country", back_populates="decks")

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

    @property
    def name(self):
        """ Getter for private attribute name """
        return self.__commander

    @name.setter
    def commander(self, value):
        """ Setter for private attribute name """

        # ensure that the value is not spaces-only and only contains allowed characters (alphabet, latin letters, and some punctuation)
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z\xC0-\xFF,' ]+$", value)
        if is_valid_name:
            self.__commander = value
        else:
            raise ValueError("Invalid commander specified: {}".format(value))

    @property
    def player_id(self):
        """ Getter for private prop player_id """
        return self.__player_id

    @player_id.setter
    def player_id(self, value):
        """ Setter for private prop player_id """
        self.__player_id = value

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
    def create():
        """ Class method that creates a new deck """
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()
        if 'commander' not in data:
            abort(400, "Missing commander")
        if 'player_id' not in data:
            abort(400, "Missing player id")

        exists = storage.get(class_name = 'Player', key = 'id', value = data["player_id"])
        if exists is None:
            abort(400, "Specified player does not exist")

        try:
            new_deck = Deck(
                name=data["name"],
                player_id=data["player_id"]
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        try:
            storage.add(new_deck)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Deck!"

        output = {
            "id": new_deck.id,
            "commander": new_deck.commander,
            "player_id": new_deck.player_id
        }

        return jsonify(output)

    @staticmethod
    def update(deck_id):
        """ Class method that updates an existing deck """
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        try:
            # update the Deck record. Only commander can be changed
            result = storage.update('Deck', deck_id, data, Deck.can_update_list)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified deck!"

        output = {
            "id": result.id,
            "commander": result.commander,
            "player_id": result.player_id
        }

        return jsonify(output)

#!/usr/bin/python
""" Deck model """

import uuid
import re
from flask import jsonify, request, abort
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from data import storage, Base

class Player(Base):
    """ Representation of player """

    can_init   = ["name"]
    can_update = ["name"]

    # Class attributes defaults
    __tablename__ = 'decks'
    id     = Column(String(64), nullable=False, primary_key=True)
    __name = Column("name", String(128), nullable=False)
    decks  = relationship("Deck", back_populates="player", cascade="delete, delete-orphan")

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
        return self.__name

    @name.setter
    def name(self, value):
        """ Setter for private attribute name """

        # ensure that the value is not spaces-only and only contains allowed characters (alphabet, latin letters, and some punctuation)
        is_valid_name = len(value.strip()) > 0 and re.search("^[a-zA-Z\xC0-\xFF,' ]+$", value)
        if is_valid_name:
            self.__name = value
        else:
            raise ValueError("Invalid nqme specified: {}".format(value))


    # --- Static methods ---
    @staticmethod
    def all():
        """ Class method that returns all players data """
        output = []

        try:
            result = storage.get(class_name = 'Player')
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load players!"

        for row in result:
            output.append({
                "id": row.id,
                "name": row.name,
            })

        return jsonify(output)

    @staticmethod
    def specific(player_id):
        """ Class method that returns a specific player's data """
        try:
            result: Player = storage.get(class_name = 'Player', key = 'id', value = player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to load Player data!"

        output = {
            "id": result[0].id,
            "commander": result[0].commander,
            "player_id": result[0].player_id
        }

        return jsonify(output)

    @staticmethod
    def create():
        """ Class method that creates a new player """
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()
        if 'name' not in data:
            abort(400, "Missing name")

        try:
            new_player = Player(
                name=data["name"]
            )
        except ValueError as exc:
            return repr(exc) + "\n"

        try:
            storage.add(new_player)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to add new Player!"

        output = {
            "id": new_player.id,
            "commander": new_player.commander,
            "player_id": new_player.player_id
        }

        return jsonify(output)

    @staticmethod
    def update(player_id):
        """ Class method that updates an existing player """
        if request.get_json() is None:
            abort(400, "Not a JSON")

        data = request.get_json()

        try:
            # update the Player record. Only name can be changed
            result = storage.update('Player', player_id, data, Player.can_update_list)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to update specified player!"

        output = {
            "id": result.id,
            "name": result.name
        }

        return jsonify(output)

    @staticmethod
    def delete(player_id):
        """ Class method that deletes an existing Player """
        try:
            # delete the Player record
            storage.delete('Player', player_id)
        except IndexError as exc:
            print("Error: ", exc)
            return "Unable to delete specified player!"

        return Player.all()

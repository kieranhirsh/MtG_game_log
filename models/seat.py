#!/usr/bin/python
""" Seat model """
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from data import Base

class Seat(Base):
    """ Representation of seat """

    all_attribs = ["id", "seat_no", "ko_turn", "deck_id", "game_id", "player_id"]
    can_init    = ["seat_no", "ko_turn", "deck_id", "game_id", "player_id"]
    can_update  = ["seat_no", "ko_turn", "deck_id", "game_id", "player_id"]

    # Class attributes defaults
    __tablename__ = 'Seats'
    id            = Column(String(64), nullable=False, primary_key=True)
    seat_no       = Column("seat_no", Integer, nullable=False)
    ko_turn       = Column("ko_turn", Integer)
    deck_id       = Column("deck_id", String(128), ForeignKey('decks.id'), nullable=False)
    game_id       = Column("game_id", String(128), ForeignKey('games.id'), nullable=False)
    player_id     = Column("player_id", String(128), ForeignKey('Players.id'), nullable=False)
    deck          = relationship("deck", back_populates="seats")
    game          = relationship("game", back_populates="seats", cascade="delete")
    player        = relationship("Player", back_populates="seats")

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

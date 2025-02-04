#!/usr/bin/python
""" Deck model """
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from data import Base

class Deck(Base):
    """ Representation of deck """

    all_attribs = ["id", "commander", "player_id"]
    can_init    = ["commander", "player_id"]
    can_update  = ["commander", "player_id"]

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

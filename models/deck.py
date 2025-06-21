#!/usr/bin/python
""" deck model """
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from data import Base

class deck(Base):
    """ Representation of deck """

    all_attribs = ["id", "deck_name", "player_id", "colour_identity_id"]
    can_init    = ["deck_name", "player_id", "colour_identity_id"]
    can_update  = ["deck_name", "player_id", "colour_identity_id"]

    # Class attributes defaults
    __tablename__      = 'decks'
    id                 = Column(String(64), nullable=False, primary_key=True)
    deck_name          = Column("deck_name", String(128), nullable=False)
    player_id          = Column("player_id", String(128), ForeignKey('Players.id'), nullable=False)
    colour_identity_id = Column("colour_identity_id", String(128), ForeignKey('colour_identities.id'), nullable=False)
    player             = relationship("Player", back_populates="decks")
    colour_identity    = relationship("colour_identity", back_populates="decks")
    seats              = relationship("Seat", back_populates="deck", cascade="delete, delete-orphan")
    games_won          = relationship("game", back_populates="winning_deck", cascade="delete, delete-orphan")

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

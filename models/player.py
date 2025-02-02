#!/usr/bin/python
""" Player model """
import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from data import Base

class Player(Base):
    """ Representation of player """

    can_init   = ["name"]
    can_update = ["name"]

    # Class attributes defaults
    __tablename__ = 'Players'
    id    = Column(String(64), nullable=False, primary_key=True)
    name  = Column("name", String(128), nullable=False)
    decks = relationship("Deck", back_populates="player", cascade="delete, delete-orphan")

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

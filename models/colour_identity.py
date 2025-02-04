#!/usr/bin/python
""" Player model """
import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from data import Base

class Colour_Identity(Base):
    """ Representation of colour identity """

    all_attribs = ["id", "colour_identity", "colours"]
    can_init    = ["colour_identity", "colours"]
    can_update  = []

    # Class attributes defaults
    __tablename__    = 'Colour_Identities'
    id               = Column(String(64), nullable=False, primary_key=True)
    colour_identity  = Column("colour_identity", String(128), nullable=False)
    colours          = Column("colours", String(128), nullable=False)
    decks            = relationship("Deck", back_populates="colour_identity", cascade="delete, delete-orphan")

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

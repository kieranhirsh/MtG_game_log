#!/usr/bin/python
""" Game model """
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from data import Base

class Game(Base):
    """ Representation of game """

    all_attribs = ["id", "game_name", "start_time", "end_time", "game_time"]
    can_init    = ["game_name", "start_time", "end_time", "game_time"]
    can_update  = ["game_name", "start_time", "end_time", "game_time"]

    # Class attributes defaults
    __tablename__ = 'Games'
    id            = Column(String(64), nullable=False, primary_key=True)
    game_name     = Column("game_name", String(1024))
    start_time    = Column("start_time", DateTime)
    end_time      = Column("end_time", DateTime)
    game_time     = Column("game_time", String(64))
    seats         = relationship("Seat", back_populates="game", cascade="delete, delete-orphan")

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

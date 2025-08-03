""" player model """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from data import Base
from models.base_model import constructor

class player(Base):
    """ Representation of player """
    all_attribs = ["id", "player_name"]
    can_init    = ["player_name"]
    can_update  = ["player_name"]

    # Class attributes defaults
    __tablename__ = 'players'
    id            = Column(String(64), nullable=False, primary_key=True)
    player_name   = Column("player_name", String(128), nullable=False)
    decks         = relationship("deck", back_populates="player", cascade="delete, delete-orphan")
    seats         = relationship("seat", back_populates="player", cascade="delete, delete-orphan")
    games_won     = relationship("game", back_populates="winning_player", cascade="delete, delete-orphan")

    # constructor
    def __init__(self, *args, **kwargs):
        constructor(self, *args, **kwargs)

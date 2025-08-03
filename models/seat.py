""" seat model """
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from data import Base
from models.base_model import constructor

class seat(Base):
    """ Representation of seat """
    all_attribs = ["id", "seat_no", "ko_turn", "deck_id", "game_id", "player_id"]
    can_init    = ["seat_no", "ko_turn", "deck_id", "game_id", "player_id"]
    can_update  = ["seat_no", "ko_turn", "deck_id", "game_id", "player_id"]

    # Class attributes defaults
    __tablename__ = 'seats'
    id            = Column(String(64), nullable=False, primary_key=True)
    seat_no       = Column("seat_no", Integer, nullable=False)
    ko_turn       = Column("ko_turn", Integer)
    deck_id       = Column("deck_id", String(128), ForeignKey('decks.id'), nullable=False)
    game_id       = Column("game_id", String(128), ForeignKey('games.id'), nullable=False)
    player_id     = Column("player_id", String(128), ForeignKey('players.id'), nullable=False)
    deck          = relationship("deck", back_populates="seats")
    game          = relationship("game", back_populates="seats", cascade="delete")
    player        = relationship("player", back_populates="seats")

    # constructor
    def __init__(self, *args, **kwargs):
        constructor(self, *args, **kwargs)

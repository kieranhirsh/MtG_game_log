""" game model """
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data import Base
from models.base_model import constructor

class game(Base):
    """ Representation of game """
    all_attribs = ["id", "game_name", "month", "year", "start_time",
                   "end_time", "winning_deck_id","winning_player_id"]
    can_init    = ["game_name", "month", "year", "start_time", "end_time",
                   "winning_deck_id", "winning_player_id"]
    can_update  = ["game_name", "month", "year", "start_time", "end_time",
                   "winning_deck_id", "winning_player_id"]

    # Class attributes defaults
    __tablename__     = 'games'
    id                = Column(String(64), nullable=False, primary_key=True)
    month             = Column("month", String(16))
    year              = Column("year", Integer)
    game_name         = Column("game_name", String(1024))
    start_time        = Column("start_time", DateTime, nullable=True)
    end_time          = Column("end_time", DateTime, nullable=True)
    winning_deck_id   = Column("winning_deck_id", String(128), ForeignKey('decks.id'), nullable=True)
    winning_player_id = Column("winning_player_id", String(128), ForeignKey('players.id'), nullable=True)
    winning_deck      = relationship("deck", back_populates="games_won")
    winning_player    = relationship("player", back_populates="games_won")
    seats             = relationship("seat", back_populates="game", cascade="delete, delete-orphan")

    # constructor
    def __init__(self, *args, **kwargs):
        constructor(self, *args, **kwargs)

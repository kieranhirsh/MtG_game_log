""" game model """
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data import Base
from models.base_model import constructor

class game(Base):
    """ Representation of game """
    all_attribs = ["id", "game_name", "start_time", "end_time"]
    can_init    = ["game_name", "start_time", "end_time"]
    can_update  = ["game_name", "start_time", "end_time"]

    # Class attributes defaults
    __tablename__     = 'games'
    id                = Column(String(64), nullable=False, primary_key=True)
    game_name         = Column("game_name", String(1024))
    start_time        = Column("start_time", DateTime, nullable=True)
    end_time          = Column("end_time", DateTime, nullable=True)
    seats             = relationship("seat", back_populates="game", cascade="delete, delete-orphan")

    # constructor
    def __init__(self, *args, **kwargs):
        constructor(self, *args, **kwargs)

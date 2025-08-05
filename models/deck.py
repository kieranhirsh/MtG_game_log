""" deck model """
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data import Base
from models.base_model import constructor

class deck(Base):
    """ Representation of deck """
    all_attribs = ["id", "deck_name", "commander_name", "partner_name", "companion_name", "edhrec_num_decks",
                   "edhrec_popularity", "last_accessed", "player_id","colour_identity_id"]
    can_init    = ["deck_name", "commander_name", "partner_name", "companion_name", "edhrec_num_decks",
                   "edhrec_popularity", "last_accessed", "player_id","colour_identity_id"]
    can_update  = ["deck_name", "commander_name", "partner_name", "companion_name", "edhrec_num_decks",
                   "edhrec_popularity", "last_accessed", "player_id","colour_identity_id"]

    # Class attributes defaults
    __tablename__      = 'decks'
    id                 = Column(String(64), nullable=False, primary_key=True)
    deck_name          = Column("deck_name", String(128), nullable=False)
    commander_name       = Column("commander_id", String(64), nullable=True)
    partner_name         = Column("partner_id", String(64), nullable=True)
    companion_name       = Column("companion_id", String(64), nullable=True)
    edhrec_num_decks   = Column("edhrec_num_decks", Integer, nullable=True)
    edhrec_popularity  = Column("edhrec_popularity", Integer, nullable=True)
    last_accessed      = Column("last_accessed", DateTime, nullable=True)
    player_id          = Column("player_id", String(64), ForeignKey('players.id'), nullable=False)
    colour_identity_id = Column("colour_identity_id", String(64), ForeignKey('colour_identities.id'), nullable=False)
    player             = relationship("player", back_populates="decks")
    colour_identity    = relationship("colour_identity", back_populates="decks")
    seats              = relationship("seat", back_populates="deck", cascade="delete, delete-orphan")
    games_won          = relationship("game", back_populates="winning_deck", cascade="delete, delete-orphan")

    # constructor
    def __init__(self, *args, **kwargs):
        constructor(self, *args, **kwargs)

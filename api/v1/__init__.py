#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

api_routes = Blueprint('api_routes', __name__, url_prefix='/api/v1')

from api.v1.colour_identities import *
from api.v1.decks import *
from api.v1.games import *
from api.v1.seats import *
from api.v1.players import *

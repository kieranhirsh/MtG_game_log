from flask import render_template
from crud.colour_identity import Colour_Identity_crud
from crud.deck import Deck_crud
from crud.player import Player_crud

def entry_not_found(page, missing_entries, method=""):
  # Initialise variables
  error_messages = []

  # Load all the data, because we don't know what we will need
  colour_identities = Colour_Identity_crud.all(True)
  decks = Deck_crud.all(True)
  players = Player_crud.all(True)

  for entry in missing_entries:
    error_messages.append("Error: Unable to find %s with %s = %s" % (entry[0], entry[1], entry[2]))

  # Return the page
  return render_template('error.html',
                         page=page,
                         method=method,
                         error_messages=error_messages,
                         colour_identities=colour_identities,
                         decks=decks,
                         players=players), 400

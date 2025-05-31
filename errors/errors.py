from flask import render_template
from crud.colour_identity import Colour_Identity_crud
from crud.deck import Deck_crud
from crud.player import Player_crud
from utils import utils

def entry_not_found(page, missing_entries, method=""):
    '''
        This function is for when an attempt is made to access a database entry that doesn't exist
    '''
    # Initialise variables
    error_messages = []

    # Load all the data, because we don't know what we will need
    all_db_data = utils.load_all_db_data()

    for entry in missing_entries:
        error_messages.append("Error: Unable to find %s with %s = %s" % (entry[0], entry[1], entry[2]))

    # Return the page
    return render_template('error.html',
                           page=page,
                           method=method,
                           error_messages=error_messages,
                           data=all_db_data), 400

def option_not_available(page, missing_entries, method=""):
    '''
        This function is for when a user requests an option that doesn't exist
    '''
    # Initialise variables
    error_messages = []

    # Load all the data, because we don't know what we will need
    all_db_data = utils.load_all_db_data()

    for entry in missing_entries:
        error_messages.append("Error: %s is not a valid %s" % (entry[0], entry[1]))

    # Return the page
    return render_template('error.html',
                           page=page,
                           method=method,
                           error_messages=error_messages,
                           data=all_db_data), 400

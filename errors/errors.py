from flask import render_template
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
        error_messages.append(f"Error: Unable to find {entry[0]} with {entry[1]} = {entry[2]}")

    # Return the page
    return render_template('error.html',
                           page=page,
                           method=method,
                           error_messages=error_messages,
                           data=all_db_data,
                           menu_data=all_db_data), 400

def option_not_available(page, missing_entries, method=""):
    '''
        This function is for when a user requests an option that doesn't exist
    '''
    # Initialise variables
    error_messages = []

    # Load all the data, because we don't know what we will need
    all_db_data = utils.load_all_db_data()

    for entry in missing_entries:
        error_messages.append(f"Error: {entry[0]} is not a valid {entry[1]}")

    # Return the page
    return render_template('error.html',
                           page=page,
                           method=method,
                           error_messages=error_messages,
                           data=all_db_data,
                           menu_data=all_db_data), 400

def card_not_found(page, details, method=""):
    '''
        This function is for when a user requests a card that we can't find with scryfall
    '''
    # Initialise variables
    error_messages = []

    # Load all the data, because we don't know what we will need
    all_db_data = utils.load_all_db_data()

    for detail in details:
        error_messages.append(detail)

    # Return the page
    return render_template('error.html',
                           page=page,
                           method=method,
                           error_messages=error_messages,
                           data=all_db_data,
                           menu_data=all_db_data), 400

def missing_form_item(page, method=""):
    '''
        This function is for when the expected form items are not found
    '''
    # Initialise variables
    error_messages = ["The expected form items were not found"]

    # Load all the data, because we don't know what we will need
    all_db_data = utils.load_all_db_data()

    # Return the page
    return render_template('error.html',
                           page=page,
                           method=method,
                           error_messages=error_messages,
                           data=all_db_data,
                           menu_data=all_db_data), 400

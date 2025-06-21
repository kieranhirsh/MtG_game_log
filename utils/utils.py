#!/usr/bin/python3
from crud.colour_identity import colour_identity_crud
from crud.deck import deck_crud
from crud.game import game_crud
from crud.player import player_crud
from crud.seat import seat_crud
from data import storage

def get_ci_data_from_dropdown_inputs(request_form):
    # initialise varaiables
    ci_abbr_string = ""
    ci_abbr_list = []

    # get the list of inputs and all colour identity data
    ci_raw_list = request_form.getlist("ci_abbr")
    all_ci = storage.get(class_name="colour_identity")

    # loop over the raw list of inputs and add its character to a string
    for abbr in ci_raw_list:
        ci_abbr_string += abbr

    # if no colour identity was selected, we need a useful string for our errors
    if not ci_abbr_string:
        desired_ci = "{none}"
    else:
        # loop over all the colour identities and add their colour abbreviations to a list
        for ci in all_ci:
            ci_abbr_list.append(ci.colours)

        # loop over this list of colour abbreviations and compare each item to the input string
        for ci_abbr in ci_abbr_list:
            # the strings are sorted so that anagrams match
            if sorted(ci_abbr) == sorted(ci_abbr_string):
                desired_ci = ci_abbr
                break

    # find the desired colour identity object (will be empty is the desired colour identity doesn't exist)
    colour_identity_data = storage.get(class_name="colour_identity", key="colours", value=desired_ci)

    return colour_identity_data, desired_ci

def load_all_db_data():
    '''
        Function that loads every table from the database.
        This exists to save my sanity every time I update the database.
    '''
    colour_identities = colour_identity_crud.all(True)
    decks = deck_crud.all(True)
    games = game_crud.all(True)
    players = player_crud.all(True)
    seats = seat_crud.all(True)

    return {
            "colour_identities": colour_identities,
            "decks": decks,
            "games": games,
            "players": players,
            "seats": seats
            }

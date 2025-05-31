#!/usr/bin/python3
from crud.colour_identity import Colour_Identity_crud
from crud.deck import Deck_crud
from crud.player import Player_crud
from data import storage

def get_ci_data_from_dropdown_inputs(request_form):
    # initialise varaiables
    ci_abbr_string = ""
    ci_abbr_list = []

    # get the list of inputs and all colour identity data
    ci_raw_list = request_form.getlist("ci_abbr")
    all_ci = storage.get(class_name="Colour_Identity")

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
    colour_identity_data = storage.get(class_name="Colour_Identity", key="colours", value=desired_ci)

    return colour_identity_data, desired_ci

def load_all_db_data():
    colour_identities = Colour_Identity_crud.all(True)
    decks = Deck_crud.all(True)
    players = Player_crud.all(True)

    return {
            "colour_identities": colour_identities,
            "decks": decks,
            "players": players
            }

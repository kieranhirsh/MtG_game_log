from crud.colour_identity import colour_identity_crud
from crud.deck import deck_crud
from crud.game import game_crud
from crud.player import player_crud
from crud.seat import seat_crud
from data import storage

def get_ci_data_from_list_of_colours(ci_raw_list):
    # initialise varaiables
    ci_abbr_string = ""

    # get the list of inputs and all colour identity data
    all_ci = storage.get(class_name="colour_identity")

    # loop over the raw list of inputs and add its character to a string
    for abbr in ci_raw_list:
        ci_abbr_string += abbr

    # if no colour identity was selected, we need a useful string for our errors
    if not ci_abbr_string:
        desired_ci = "{none}"
    else:
        # loop over all the colour identities and compare each string of colours to the input string
        for ci in all_ci:
            # the strings are sorted so that anagrams match
            if sorted(set(ci.colours)) == sorted(set(ci_abbr_string)):
                desired_ci = ci.colours
                break

    # find the desired colour identity object (will be empty if the desired colour identity doesn't exist)
    colour_identity_data = storage.get(class_name="colour_identity", key="colours", value=desired_ci)

    # return the colour identity object, as well as the colour identity abbreviation
    return colour_identity_data, desired_ci

def get_deck_data_from_form_inputs(deck_from_form):
    # fom data comes in in the form "deck_name (owner_name)"
    # so, we split the form data at the open bracket
    split_deck = deck_from_form.split("(")

    # get the deck name is the first word, minues the space at the end
    # owner name is the second word, minus the close bracket at the end
    deck_name = split_deck[0][:-1]
    owner_name = split_deck[1][:-1]

    # also build the query tree here
    query_tree = {
        "op": "and",
        "clauses": [
            {
                "model": "deck",
                "key": "deck_name",
                "op": "==",
                "value": deck_name
            },
            {
                "model": "player",
                "key": "player_name",
                "op": "==",
                "value": owner_name
            }
        ]
    }

    # retun the deck name and owner name
    return deck_name, owner_name, query_tree

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

#!/usr/bin/python3
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

def find_number_of_colours_of_deck(deck_model):
    # get the colour identity object associated with the input deck objoect
    deck_ci_model = getattr(deck_model, "colour_identity")

    # return the number of colours in the colour identity
    return find_number_of_colours_of_ci(deck_ci_model)

def find_number_of_colours_of_ci(ci_model):
    # get the colours of the colour identity
    ci_colours = getattr(ci_model, "colours")

    # count the number of colours
    ci_num_colours = len(ci_colours)
    # need to hard code an exception here for colourless decks since len("c") = 1, but we want 0
    if ci_colours == "c":
        ci_num_colours = 0

    return ci_num_colours

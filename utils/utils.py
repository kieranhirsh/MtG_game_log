#!/usr/bin/python3
from data import storage

def get_ci_data_from_dropdown_inputs(request_form):
    ci_raw_list = request_form.getlist("ci_abbr")
    ci_abbr_string = ""
    for abbr in ci_raw_list:
        ci_abbr_string += abbr
    all_ci = storage.get(class_name="Colour_Identity")
    ci_abbr_list = []
    for ci in all_ci:
        ci_abbr_list.append(ci.colours)
    for ci_abbr in ci_abbr_list:
        if sorted(ci_abbr) == sorted(ci_abbr_string):
            desired_ci = ci_abbr
    colour_identity_data = storage.get(class_name="Colour_Identity", key="colours", value=desired_ci)
    return colour_identity_data, desired_ci
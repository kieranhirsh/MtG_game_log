#!/usr/bin/python
""" Colour Identity validation """
import re

class Colour_Identity_validator():
    def is_valid(new_colour_identity):
        # check all inputs are valid
        Colour_Identity_validator.valid_ci_name(new_colour_identity.ci_name)
        Colour_Identity_validator.valid_colours(new_colour_identity.colours)
        Colour_Identity_validator.valid_num_colours(new_colour_identity.num_colours)

        # if all checks are passed, we're good to go
        return True

    def valid_ci_name(ci_name):
        # there are only 32 valid colour identities, check that this is one of them
        allowed_colour_identities = [
            "Colourless",
            "Mono-white",
            "Mono-blue",
            "Mono-black",
            "Mono-red",
            "Mono-green",
            "Azorius",
            "Dimir",
            "Rakdos",
            "Gruul",
            "Selesnya",
            "Orzhov",
            "Golgari",
            "Simic",
            "Izzet",
            "Boros",
            "Bant",
            "Esper",
            "Grixis",
            "Jund",
            "Naya",
            "Mardu",
            "Temur",
            "Abzan",
            "Jeskai",
            "Sultai",
            "Glint-Eye",
            "Dune-Brood",
            "Ink-Treader",
            "Witch-Maw",
            "Yore-Tiller",
            "Rainbow"
        ]
        if ci_name not in allowed_colour_identities:
            raise ValueError("Invalid colour identiy specified: {}".format(ci_name))

        return True

    def valid_colours(colours):
        # there are only 5 valid colours, check that the colours are a subset of those
        # use regex to check this. this requires lookaheads and I don't get it, but it works
        # put the regex into regex101.com for a better explanation than I'll ever be able to give
        if not re.search("(^(?=[^w]*w?[^w]*$)(?=[^u]*u?[^u]*$)(?=[^b]*b?[^b]*$)(?=[^r]*r?[^r]*$)(?=[^g]*g?[^g]*$)[wubrg]+$|^$)", colours):
            raise ValueError("Invalid colours specified: {}".format(colours))

        return True

    def valid_num_colours(num_colours):
        # there are only 5 valid colours, check that the colours are a subset of those
        # use regex to check this. this requires lookaheads and I don't get it, but it works
        # put the regex into regex101.com for a better explanation than I'll ever be able to give
        if not num_colours % 1 == 0:
            raise ValueError("Invalid colours specified: {}".format(num_colours))

        return True

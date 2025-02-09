""" objects that handles all default RestFul API actions for Colour Identity """
from flask import jsonify
from api.v1 import api_routes
from crud.colour_identity import Colour_Identity_crud

@api_routes.route('/colour_identities', methods=["POST"])
def colour_identities_post():
    """ posts data for new colour identity then returns the colour identity data """
    return jsonify(Colour_Identity_crud.create())

@api_routes.route('/colour_identities', methods=["GET"])
def colour_identities_get():
    """ returns colour identities data """
    return jsonify(Colour_Identity_crud.all())

@api_routes.route('/colour_identities/<colour_identity_id>', methods=["GET"])
def colour_identities_get_specific(colour_identity_id):
    """ returns specific colour identity data """
    return jsonify(Colour_Identity_crud.specific(colour_identity_id))

@api_routes.route('/colour_identities/<colour_identity_id>', methods=["PUT"])
def colour_identities_edit(colour_identity_id):
    """ updates existing colour identity data using specified id """
    return jsonify(Colour_Identity_crud.update(colour_identity_id))

@api_routes.route('/colour_identities/<colour_identity_id>/decks', methods=["GET"])
def colour_identities_get_decks(colour_identity_id):
    """ returns all decks with a given colour identity """
    return jsonify(Colour_Identity_crud.get_child_data(colour_identity_id, child_type="Deck"))

@api_routes.route('/colour_identities/<colour_identity_id>', methods=["DELETE"])
def colour_identities_delete(colour_identity_id):
    """ deletes existing colour identity data using specified id """
    return jsonify(Colour_Identity_crud.delete(colour_identity_id))

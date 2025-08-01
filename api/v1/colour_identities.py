""" objects that handles all default RestFul API actions for Colour Identity """
from flask import jsonify
from api.v1 import api_routes
from crud.colour_identity import colour_identity_crud

@api_routes.route('/colour_identities', methods=["POST"])
def colour_identities_post():
    """ posts data for new colour identity then returns the colour identity data """
    return jsonify(colour_identity_crud.create())

@api_routes.route('/colour_identities', methods=["GET"])
def colour_identities_get():
    """ returns colour identities data """
    return jsonify(colour_identity_crud.all())

@api_routes.route('/colour_identities/<colour_identity_id>', methods=["GET"])
def colour_identities_get_specific(colour_identity_id):
    """ returns specific colour identity data """
    return jsonify(colour_identity_crud.specific('id', colour_identity_id))

@api_routes.route('/colour_identities/<colour_identity_id>', methods=["PUT"])
def colour_identities_edit(colour_identity_id):
    """ updates existing colour identity data using specified id """
    return jsonify(colour_identity_crud.update(colour_identity_id))

@api_routes.route('/colour_identities/<colour_identity_id>/decks', methods=["GET"])
def colour_identities_get_decks(colour_identity_id):
    """ returns all decks with a given colour identity """
    return jsonify(colour_identity_crud.get_child_data(colour_identity_id, child_type="deck"))

@api_routes.route('/colour_identities/<colour_identity_id>', methods=["DELETE"])
def colour_identities_delete(colour_identity_id):
    """ deletes existing colour identity data using specified id """
    return jsonify(colour_identity_crud.delete(colour_identity_id))

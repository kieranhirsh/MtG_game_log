#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify
from api.v1 import api_routes
from data import storage
from crud.colour_identity import Colour_Identity_crud
from crud.deck import Deck_crud
from crud.player import Player_crud

app = Flask(__name__)
app.register_blueprint(api_routes)

@app.route('/')
def index():
    """ Landing page for the site """

    return render_template('index.html')

@app.route('/input', methods=['GET', 'POST'])
def input():
    """ Data is inputted here """
    if request.method == 'POST':
        # First add the new item to the database
        input_type = request.form["type"]

        # this desperately wants to be a select case, but I'm using Python 3.8 :(
        if input_type == "player":
            new_player = {
                "name": request.form["name"]
            }

            Player_crud.create(data=jsonify(new_player))
        elif input_type == "deck":
            owner_name = request.form["owner"]
            owner_data = storage.get(class_name="Player", key="name", value=owner_name)

            colour_identity = request.form["colour_identity"]
            colour_identity_data = storage.get(class_name="Colour_Identity", key="colour_identity", value=colour_identity)

            new_deck = {
                "commander": request.form["commander"],
                "player_id": owner_data[0].id,
                "colour_identity_id": colour_identity_data[0].id
                }

            Deck_crud.create(data=jsonify(new_deck))

    # Then load the data we need before passing it to the template
    players = Player_crud.all(True)
    colour_identities = Colour_Identity_crud.all(True)

    return render_template('input.html', colour_identities=colour_identities, players=players)

@app.route('/data', methods=['GET'])
def data_get():
    """ Spreadsheets are called here """
    return render_template('data.html')

@app.route('/data', methods=['POST'])
def data_post():
    """ Spreadsheets are displayed here """
    colour_identity_data = []

    # Load the data we need before passing it to the template
    colour_identities = Colour_Identity_crud.all(True)
    decks = Deck_crud.all(True)
    players = Player_crud.all(True)

    for colour_identity in colour_identities:
        print("colour_identity = ", colour_identity)
        num_decks = len(Colour_Identity_crud.get_child_data(colour_identity.id, "decks", True))

        colour_identity_data.append({
            "name": colour_identity.colour_identity,
            "number_of_decks": num_decks
        })

    return render_template(
        'data.html',
        colour_identities=colour_identity_data,
        decks=decks,
        players=players
    )

@app.route('/graphs')
def graphs():
    """ Graphs are displayed here """
    # Load the data we need before passing it to the template
    colour_identities = Colour_Identity_crud.all(True)
    decks = Deck_crud.all(True)
    players = Player_crud.all(True)

    return render_template(
        'graphs.html',
        colour_identities=colour_identities,
        decks=decks,
        players=players
    )

# Set debug=True for the server to auto-reload when there are changes
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

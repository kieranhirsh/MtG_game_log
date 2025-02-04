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

@app.route('/input')
def input():
    """ Landing page for inputting data """
    return render_template('input.html')

@app.route('/input/decks', methods=['POST'])
def input_deck():
    """ Data is inputted here """
    if request.method == "POST":
        player_name = request.form["name"]
        player_data = storage.get(class_name="Player", key="name", value=player_name)

        colour_identity = request.form["colour_identity"]
        colour_identity_data = storage.get(class_name="Colour_Identity", key="colour_identity", value=colour_identity)

        new_player = {
            "commander": request.form["commander"],
            "player_id": player_data[0].id,
            "colour_identity_id": colour_identity_data[0].id
            }

        Deck_crud.create(data=jsonify(new_player))

    return render_template('input.html')

@app.route('/input/players', methods=['POST'])
def input_player():
    """ Data is inputted here """
    if request.method == "POST":
        new_player = {
            "name": request.form["name"]
        }

        Player_crud.create(data=jsonify(new_player))

    return render_template('input.html')

@app.route('/data')
def data():
    """ Spreadsheets are displayed here """
    # Load the data we need before passing it to the template
    colour_identities = Colour_Identity_crud.all(True)
    decks = Deck_crud.all(True)
    players = Player_crud.all(True)

    return render_template(
        'data.html',
        colour_identities=colour_identities,
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

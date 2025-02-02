#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify
from api.v1 import api_routes
from data import storage
from models.deck import Deck
from models.player import Player

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

@app.route('/input/players', methods=['POST'])
def input_player():
    """ Data is inputted here """
    if request.method == "POST":
        new_player = {
            "name": request.form["name"]
        }

        Player.create(data=jsonify(new_player))

    return render_template('input.html')

@app.route('/input/decks', methods=['POST'])
def input_deck():
    """ Data is inputted here """
    if request.method == "POST":
        player_name = request.form["name"]
        player_data = storage.get(class_name="Player", key="name", value=player_name)

        new_player = {
            "player_id": player_data[0].id,
            "commander": request.form["commander"]
            }

        Deck.create(data=jsonify(new_player))

    return render_template('input.html')

@app.route('/data')
def data():
    """ Spreadsheets are displayed here """
    # Load the data we need before passing it to the template
    decks = Deck.all(True)
    players = Player.all(True)

    return render_template('data.html', decks=decks, players=players)

@app.route('/graphs')
def graphs():
    """ Graphs are displayed here """
    # Load the data we need before passing it to the template
    decks = Deck.all(True)
    players = Player.all(True)

    return render_template('graphs.html', decks=decks, players=players)

# Set debug=True for the server to auto-reload when there are changes
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

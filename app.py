#!/usr/bin/python3
from flask import Flask, render_template, request, jsonify
from api.v1 import api_routes
from data import storage
from crud.colour_identity import Colour_Identity_crud
from crud.deck import Deck_crud
from crud.player import Player_crud
from graphs import pie_charts, bar_charts

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
                "player_name": request.form["player_name"]
            }

            Player_crud.create(data=jsonify(new_player))
        elif input_type == "deck":
            owner_name = request.form["owner"]
            owner_data = storage.get(class_name="Player", key="player_name", value=owner_name)

            ci_name = request.form["ci_name"]
            colour_identity_data = storage.get(class_name="Colour_Identity", key="ci_name", value=ci_name)

            new_deck = {
                "deck_name": request.form["deck_name"],
                "player_id": owner_data[0].id,
                "colour_identity_id": colour_identity_data[0].id
                }

            Deck_crud.create(data=jsonify(new_deck))

    # Then load the data we need before passing it to the template
    colour_identities = Colour_Identity_crud.all(True)
    players = Player_crud.all(True)

    return render_template('input.html', method="create", colour_identities=colour_identities, players=players)

@app.route('/input/edit', methods=['GET', 'POST'])
def input_edit():
    """ Data is edited here """
    if request.method == 'POST':
        # First add the new item to the database
        input_type = request.form["type"]

        # this desperately wants to be a select case, but I'm using Python 3.8 :(
        if input_type == "player":
            player_to_edit = Player_crud.specific('player_name', request.form['player_name'])
            new_player_data = {}
            if request.form["new_player_name"]:
                new_player_data.update({
                    "player_name": request.form["new_player_name"]
                })

            Player_crud.update(player_to_edit["id"], jsonify(new_player_data))
        elif input_type == "deck":
            deck_to_edit = Deck_crud.specific('deck_name', request.form['deck_name'])
            new_deck_data = {}
            if request.form["new_deck_name"]:
                new_deck_data.update({
                    "deck_name": request.form["new_deck_name"]
                })
            if request.form["owner"]:
                owner_name = request.form["owner"]
                owner_data = storage.get(class_name="Player", key="player_name", value=owner_name)

                new_deck_data.update({
                    "player_id": owner_data[0].id
                })
            if request.form["ci_name"]:
                ci_name = request.form["ci_name"]
                colour_identity_data = storage.get(class_name="Colour_Identity", key="ci_name", value=ci_name)

                new_deck_data.update({
                    "colour_identity_id": colour_identity_data[0].id
                })

            Deck_crud.update(deck_to_edit["id"], jsonify(new_deck_data))

    # Then load the data we need before passing it to the template
    colour_identities = Colour_Identity_crud.all(True)
    decks = Deck_crud.all(True)
    players = Player_crud.all(True)

    return render_template('input.html', method="edit", colour_identities=colour_identities, decks=decks, players=players)

@app.route('/input/delete', methods=['GET', 'POST'])
def input_delete():
    """ Data is deleted here """
    if request.method == 'POST':
        # First add the new item to the database
        input_type = request.form["type"]

        # this desperately wants to be a select case, but I'm using Python 3.8 :(
        if input_type == "player":
            player_to_delete = Player_crud.specific('player_name', request.form['player_name'])
            Player_crud.delete(player_to_delete["id"])
        elif input_type == "deck":
            deck_to_delete = Deck_crud.specific('deck_name', request.form['deck_name'])
            Deck_crud.delete(deck_to_delete["id"])

    # Then load the data we need before passing it to the template
    decks = Deck_crud.all(True)
    players = Player_crud.all(True)

    return render_template('input.html', method="delete", decks=decks, players=players)

@app.route('/data', methods=['GET'])
def data_get():
    """ Spreadsheets are called here """
    # Load the data we need before passing it to the template
    colour_identities = Colour_Identity_crud.all(True)
    players = Player_crud.all(True)

    return render_template('data.html', colour_identities=colour_identities, players=players)

@app.route('/data', methods=['POST'])
def data_post():
    """ Spreadsheets are displayed here """
    # Load the data we need before passing it to the template
    colour_identities = Colour_Identity_crud.all(True)
    players = Player_crud.all(True)

    # this desperately wants to be a select case, but I'm using Python 3.8 :(
    if request.form["type"] == "colour_identity":
        colour_identity_data = []

        # if we have a restriction on the player name
        if request.form['player_name']:
            # loop over all colour identities
            for colour_identity in colour_identities:
                # find all decks of with the given colour identity
                colour_identity_decks = Colour_Identity_crud.get_child_data(colour_identity.id, "Deck", True)
                decks_to_remove = []

                # loop over those decks
                for deck in colour_identity_decks:
                    # if they have the wrong owner, add them of the list of decks to remove
                    if deck.player.player_name != request.form['player_name']:
                        decks_to_remove.append(deck)

                # loop over our list of decks to remove and remove them from our list of all decks
                for deck_to_remove in decks_to_remove:
                    colour_identity_decks.remove(deck_to_remove)

                # find the number of decks of the given colour identity deck
                num_decks = len(colour_identity_decks)

                # and finally, append all the relevant data that has been requested
                colour_identity_data.append({
                    "ci_name": colour_identity.ci_name,
                    "number_of_decks": num_decks
                })
        else:
            for colour_identity in colour_identities:
                # if we have no restriction the number of decks is just the length of the array
                num_decks = len(Colour_Identity_crud.get_child_data(colour_identity.id, "Deck", True))

                colour_identity_data.append({
                    "ci_name": colour_identity.ci_name,
                    "number_of_decks": num_decks
                })

        return render_template(
            'data.html',
            data_type="colour_identity",
            colour_identities=colour_identity_data,
            players=players
        )
    elif request.form["type"] == "deck":
        decks = Deck_crud.all(True)
        restrictions = []

        for form_item in request.form:
            # this wants to be a select case, but I'm using Python 3.8 :(
            if form_item == "player_name":
                class_type = "Player"
            elif form_item == "ci_name":
                class_type = "Colour_Identity"

            if form_item != "type" and request.form[form_item]:
                restrictions.append({
                    "class_type": class_type,
                    "key": form_item,
                    "value": request.form[form_item]
                })

        if restrictions:
            deck_data = decks
            decks_to_remove = []

            for deck in deck_data:
                for restriction in restrictions:
                    parent_data = Deck_crud.get_parent_data(deck.id, restriction["class_type"], True)
                    if getattr(parent_data[0], restriction["key"]) != restriction["value"]:
                        decks_to_remove.append(deck)
                        break

            for deck_to_remove in decks_to_remove:
                deck_data.remove(deck_to_remove)
        else:
            deck_data = decks

        return render_template(
            'data.html',
            data_type="deck",
            colour_identities=colour_identities,
            decks=deck_data,
            players=players
        )
    elif request.form["type"] == "player":
        player_data = []

        # if we have a restriction on the colour identity name
        if request.form['ci_name']:

            # loop over all players
            for player in players:
                # find all decks owned by a given player
                player_decks = Player_crud.get_child_data(player.id, "Deck", True)
                decks_to_remove = []

                # loop over those decks
                for deck in player_decks:
                    # if they have the wrong colour identity, add them of the list of decks to remove
                    if deck.colour_identity.ci_name != request.form['ci_name']:
                        decks_to_remove.append(deck)

                # loop over our list of decks to remove and remove them from our list of all decks
                for deck_to_remove in decks_to_remove:
                    player_decks.remove(deck_to_remove)

                # find the number of decks the given player owns
                num_decks = len(player_decks)

                # and finally, append all the relevant data that has been requested
                player_data.append({
                    "player_name": player.player_name,
                    "number_of_decks": num_decks
                })
        else:
            for player in players:
                # if we have no restriction the number of decks is just the length of the array
                num_decks = len(Player_crud.get_child_data(player.id, "Deck", True))

                player_data.append({
                    "player_name": player.player_name,
                    "number_of_decks": num_decks
                })

        return render_template(
            'data.html',
            data_type="player",
            colour_identities=colour_identities,
            players=player_data
        )

    return render_template('data.html', colour_identities=colour_identities, players=players)

@app.route('/graphs')
def graphs():
    """ Graphs are displayed here """
    # Load the data we need before passing it to the template
    colour_identities = Colour_Identity_crud.all(True)
    decks = Deck_crud.all(True)
    players = Player_crud.all(True)

    player_names = []
    number_of_decks = []

    for player in players:
        player_names.append(player.player_name)
        number_of_decks.append(len(player.decks))

    pie_chart = pie_charts.make_pie_chart(player_names, number_of_decks, "Number of Decks per Player")
    bar_chart = bar_charts.make_bar_chart(player_names, number_of_decks, "Player Name", "Number of Decks", "Number of Decks per Player")

    return render_template(
        'graphs.html',
        graph_type="example",
        pie_chart=pie_chart,
        bar_chart=bar_chart
    )

@app.route('/graphs/bar')
def graphs_bar():
    """ Graphs are displayed here """
    print("request = ", request.form)
    # Load the data we need before passing it to the template
    colour_identities = Colour_Identity_crud.all(True)
    decks = Deck_crud.all(True)
    players = Player_crud.all(True)

    player_names = []
    number_of_decks = []

    for player in players:
        player_names.append(player.player_name)
        number_of_decks.append(len(player.decks))

    pie_chart = pie_charts.make_pie_chart(player_names, number_of_decks, "Number of Decks per Player")
    bar_chart = bar_charts.make_bar_chart(player_names, number_of_decks, "Player Name", "Number of Decks", "Number of Decks per Player")

    return render_template(
        'graphs.html',
        graph_type="bar",
        colour_identities=colour_identities,
        decks=decks,
        players=players,
        pie_chart=pie_chart,
        bar_chart=bar_chart
    )


@app.route('/graphs/pie')
def graphs_pie():
    """ Graphs are displayed here """
    print("request = ", request.form)
    # Load the data we need before passing it to the template
    colour_identities = Colour_Identity_crud.all(True)
    decks = Deck_crud.all(True)
    players = Player_crud.all(True)

    player_names = []
    number_of_decks = []

    for player in players:
        player_names.append(player.player_name)
        number_of_decks.append(len(player.decks))

    pie_chart = pie_charts.make_pie_chart(player_names, number_of_decks, "Number of Decks per Player")
    bar_chart = bar_charts.make_bar_chart(player_names, number_of_decks, "Player Name", "Number of Decks", "Number of Decks per Player")

    return render_template(
        'graphs.html',
        graph_type="pie",
        colour_identities=colour_identities,
        decks=decks,
        players=players,
        pie_chart=pie_chart,
        bar_chart=bar_chart
    )

# Set debug=True for the server to auto-reload when there are changes
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

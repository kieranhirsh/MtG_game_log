#!/usr/bin/python3
import importlib
from flask import Flask, render_template, request, jsonify
from api.v1 import api_routes
from data import storage
from errors import errors
from crud.colour_identity import Colour_Identity_crud
from crud.deck import Deck_crud
from crud.player import Player_crud
from graphs import pie_charts, xy_graphs

app = Flask(__name__)
app.register_blueprint(api_routes)

@app.route('/')
def index():
    """ Landing page for the site """

    return render_template('index.html')

@app.route('/hack')
def hack():
    """ access main security grid """

    return render_template('hack.html')

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
            call_error = False
            missing_entries = []

            owner_name = request.form["owner"]
            owner_data = storage.get(class_name="Player", key="player_name", value=owner_name)
            if not owner_data:
                call_error = True
                missing_entries.append(["Player", "player_name", owner_name])

            ci_name_raw = request.form["ci_name"]
            ci_name = ci_name_raw.split(' (', 1)[0]
            colour_identity_data = storage.get(class_name="Colour_Identity", key="ci_name", value=ci_name)
            if not colour_identity_data:
                call_error = True
                missing_entries.append(["Colour_Identity", "ci_name", ci_name])

            if call_error:
                return errors.entry_not_found('input.html', 'create', missing_entries)

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
            try:
                player_to_edit = Player_crud.specific('player_name', request.form['player_name'])
            except:
                return errors.entry_not_found('input.html', 'edit', [['Player', 'player_name', request.form['player_name']]])

            new_player_data = {}
            if request.form["new_player_name"]:
                new_player_data.update({
                    "player_name": request.form["new_player_name"]
                })

            Player_crud.update(player_to_edit["id"], jsonify(new_player_data))
        elif input_type == "deck":
            try:
                deck_to_edit = Deck_crud.specific('deck_name', request.form['deck_name'])
            except:
                return errors.entry_not_found('input.html', 'edit', [['Deck', 'deck_name', request.form['deck_name']]])

            new_deck_data = {}
            call_error = False
            missing_entries = []

            if request.form["new_deck_name"]:
                new_deck_data.update({
                    "deck_name": request.form["new_deck_name"]
                })
            if request.form["owner"]:
                owner_name = request.form["owner"]
                owner_data = storage.get(class_name="Player", key="player_name", value=owner_name)

                if owner_data:
                    new_deck_data.update({
                        "player_id": owner_data[0].id
                    })
                else:
                    call_error = True
                    missing_entries.append(["Player", "player_name", owner_name])
            if request.form["ci_name"]:
                ci_name_raw = request.form["ci_name"]
                ci_name = ci_name_raw.split(' (', 1)[0]
                colour_identity_data = storage.get(class_name="Colour_Identity", key="ci_name", value=ci_name)

                if colour_identity_data:
                    new_deck_data.update({
                        "colour_identity_id": colour_identity_data[0].id
                    })
                else:
                    call_error = True
                    missing_entries.append(["Colour_Identity", "ci_name", ci_name])

            if call_error:
                return errors.entry_not_found('input.html', 'edit', missing_entries)

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
        # This dict maps an input, taken from the dropdown menu, to the relevant crud class
        module_names = {
            "deck": Deck_crud,
            "player": Player_crud
        }

        # Find the type of data to delete
        input_type = request.form["type"]

        # Find the specific entry to delete, and either delete it or return and error
        try:
            entry_to_delete = module_names[input_type].specific("%s_name" % input_type,
                                                                request.form["%s_name" % input_type])
        except:
            return errors.entry_not_found('input.html', 'delete', [[input_type,
                                                                    "%s_name" % input_type,
                                                                    request.form["%s_name" % input_type]]])
        module_names[input_type].delete(entry_to_delete['id'])

    # Load the data we need before passing it to the template
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
                    "colours": colour_identity.colours,
                    "number_of_decks": num_decks
                })
        else:
            for colour_identity in colour_identities:
                # if we have no restriction the number of decks is just the length of the array
                num_decks = len(Colour_Identity_crud.get_child_data(colour_identity.id, "Deck", True))

                colour_identity_data.append({
                    "ci_name": colour_identity.ci_name,
                    "colours": colour_identity.colours,
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
            if form_item != "type" and request.form[form_item]:
                value = request.form[form_item]

                # this wants to be a select case, but I'm using Python 3.8 :(
                if form_item == "player_name":
                    class_type = "Player"
                elif form_item == "ci_name":
                    class_type = "Colour_Identity"
                    value = value.split(' (', 1)[0]

                restrictions.append({
                    "class_type": class_type,
                    "key": form_item,
                    "value": value
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
        if request.form["ci_name"]:
            ci_name_raw = request.form["ci_name"]
            ci_name = ci_name_raw.split(' (', 1)[0]

            # loop over all players
            for player in players:
                # find all decks owned by a given player
                player_decks = Player_crud.get_child_data(player.id, "Deck", True)
                decks_to_remove = []

                # loop over those decks
                for deck in player_decks:
                    # if they have the wrong colour identity, add them of the list of decks to remove
                    if deck.colour_identity.ci_name != ci_name:
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

@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    """ Graphs are displayed here """
    # Load the data we need before passing it to the template
    if request.method == 'GET':
        deck_data = Deck_crud.all(True)

        plt_data = {}

        for ii in list(range(0,6)):
            plt_data.update({"%s colours" % ii: 0})

        for deck in deck_data:
            deck_ci_model = getattr(deck, "colour_identity")
            deck_colours = getattr(deck_ci_model, "colours")
            deck_num_colours = len(deck_colours)
            plt_data["%s colours" % deck_num_colours] += 1

        number_of_colours = list(plt_data.keys())
        number_of_decks = list(plt_data.values())

        example_bar_chart = xy_graphs.make_xy_graph("bar", number_of_colours, number_of_decks, "Number of Colours", "Number of Decks", "Number of Decks per Number of Colours")
        example_pie_chart = pie_charts.make_pie_chart(number_of_colours, number_of_decks, "Number of Decks per Number of Colours")

        return render_template(
            'graphs.html',
            graph_type="example",
            example_bar_chart=example_bar_chart,
            example_pie_chart=example_pie_chart
        )
    elif request.method == 'POST':
        model_names = {
            "deck": {
                "file": "deck",
                "class": "Deck_crud",
                "name_column": "deck_name"
            }
        }
        titles = {
            "colour": "Colour",
            "colour identity": "Colour Identity",
            "deck": "Number of Decks",
            "number of colours": "Number of Colours",
            "number of decks": "Number of Decks",
            "owner": "Player"
        }

        if request.form['type'] == "bar":
            if request.form["bar_data"] not in list(model_names.keys()):
                raise ValueError("Incorrect Data Type specified: %s" % request.form["bar_data"])

            if "no_zeroes" in request.form:
                no_zeroes = True
            else:
                no_zeroes = False

            crud_file = importlib.import_module("crud." + model_names[request.form["bar_data"]]["file"])
            crud_class = getattr(crud_file, model_names[request.form["bar_data"]]["class"])
            data = crud_class.all(True)

            xy_data = {}

            # this wants to be a select case, but I'm using Python 3.8 :(
            if request.form["bar_x"] == "colour":
                xy_data = {
                    "colourless" : 0,
                    "white" : 0,
                    "blue" : 0,
                    "black" : 0,
                    "red" : 0,
                    "green" : 0
                }

                if request.form["bar_y"] == "number of decks":
                    for datum in data:
                        datum_ci_model = getattr(datum, "colour_identity")
                        datum_colours = getattr(datum_ci_model, "colours")
                        if not datum_colours:
                            xy_data["colourless"] += 1
                            continue
                        if "w" in datum_colours:
                            xy_data["white"] += 1
                        if "u" in datum_colours:
                            xy_data["blue"] += 1
                        if "b" in datum_colours:
                            xy_data["black"] += 1
                        if "r" in datum_colours:
                            xy_data["red"] += 1
                        if "g" in datum_colours:
                            xy_data["green"] += 1
                else:
                    raise ValueError("Incorrect Y axis specified: %s" % request.form["bar_y"])
            elif request.form["bar_x"] == "colour identity":
                colour_identities = Colour_Identity_crud.all(True)

                for colour_identity in colour_identities:
                    ci_name = getattr(colour_identity, "ci_name")
                    ci_colours = getattr(colour_identity, "colours")
                    xy_label = ci_name + " (" + ci_colours + ")"
                    xy_data.update({xy_label: 0})

                if request.form["bar_y"] == "number of decks":
                    for datum in data:
                        datum_ci_model = getattr(datum, "colour_identity")
                        datum_ci_name = getattr(datum_ci_model, "ci_name") + " (" + getattr(datum_ci_model, "colours") + ")"
                        xy_data[datum_ci_name] += 1
                else:
                    raise ValueError("Incorrect Y axis specified: %s" % request.form["bar_y"])
            elif request.form["bar_x"] == "number of colours":
                for ii in list(range(0,6)):
                    xy_data.update({"%s colours" % ii: 0})

                if request.form["bar_y"] == "number of decks":
                    for datum in data:
                        datum_ci_model = getattr(datum, "colour_identity")
                        datum_colours = getattr(datum_ci_model, "colours")
                        datum_num_colours = len(datum_colours)
                        xy_data["%s colours" % datum_num_colours] += 1
                else:
                    raise ValueError("Incorrect Y axis specified: %s" % request.form["bar_y"])
            elif request.form["bar_x"] == "owner":
                players = Player_crud.all(True)

                for player in players:
                    player_name = getattr(player, "player_name")
                    xy_data.update({player_name: 0})

                if request.form["bar_y"] == "number of decks":
                    for datum in data:
                        datum_player_model = getattr(datum, "player")
                        datum_owner = getattr(datum_player_model, "player_name")
                        xy_data[datum_owner] += 1
                else:
                    raise ValueError("Incorrect Y axis specified: %s" % request.form["bar_y"])
            else:
                raise ValueError("Incorrect Slices specified: %s" % request.form["pie_divisions"])

            x_values = list(xy_data.keys())
            y_values = list(xy_data.values())

            plt_graph = xy_graphs.make_xy_graph("bar",
                                                x_values,
                                                y_values,
                                                titles[request.form["bar_x"]],
                                                titles[request.form["bar_y"]],
                                                titles[request.form["bar_y"]] + " per " + titles[request.form["bar_x"]],
                                                no_zeroes)

        elif request.form['type'] == "pie":
            if request.form["pie_data"] not in list(model_names.keys()):
                raise ValueError("Incorrect Data Type specified: %s" % request.form["pie_data"])

            crud_file = importlib.import_module("crud." + model_names[request.form["pie_data"]]["file"])
            crud_class = getattr(crud_file, model_names[request.form["pie_data"]]["class"])
            data = crud_class.all(True)

            pie_data = {}

            # this wants to be a select case, but I'm using Python 3.8 :(
            if request.form["pie_divisions"] == "colour":
                pie_data = {
                    "colourless" : 0,
                    "white" : 0,
                    "blue" : 0,
                    "black" : 0,
                    "red" : 0,
                    "green" : 0
                }

                for datum in data:
                    datum_ci_model = getattr(datum, "colour_identity")
                    datum_colours = getattr(datum_ci_model, "colours")
                    if not datum_colours:
                        pie_data["colourless"] += 1
                        continue
                    if "w" in datum_colours:
                        pie_data["white"] += 1
                    if "u" in datum_colours:
                        pie_data["blue"] += 1
                    if "b" in datum_colours:
                        pie_data["black"] += 1
                    if "r" in datum_colours:
                        pie_data["red"] += 1
                    if "g" in datum_colours:
                        pie_data["green"] += 1
            elif request.form["pie_divisions"] == "colour identity":
                colour_identities = Colour_Identity_crud.all(True)

                for colour_identity in colour_identities:
                    ci_name = getattr(colour_identity, "ci_name")
                    ci_colours = getattr(colour_identity, "colours")
                    pie_label = ci_name + " (" + ci_colours + ")"
                    pie_data.update({pie_label: 0})

                for datum in data:
                    datum_ci_model = getattr(datum, "colour_identity")
                    datum_ci_name = getattr(datum_ci_model, "ci_name") + " (" + getattr(datum_ci_model, "colours") + ")"
                    pie_data[datum_ci_name] += 1
            elif request.form["pie_divisions"] == "number of colours":
                for ii in list(range(0,6)):
                    pie_data.update({"%s colours" % ii: 0})

                for datum in data:
                    datum_ci_model = getattr(datum, "colour_identity")
                    datum_colours = getattr(datum_ci_model, "colours")
                    datum_num_colours = len(datum_colours)
                    pie_data["%s colours" % datum_num_colours] += 1
            elif request.form["pie_divisions"] == "owner":
                players = Player_crud.all(True)

                for player in players:
                    player_name = getattr(player, "player_name")
                    pie_data.update({player_name: 0})

                for datum in data:
                    datum_player_model = getattr(datum, "player")
                    datum_owner = getattr(datum_player_model, "player_name")
                    pie_data[datum_owner] += 1
            else:
                raise ValueError("Incorrect Slices specified: %s" % request.form["pie_divisions"])

            labels = list(pie_data.keys())
            values = list(pie_data.values())

            plt_graph = pie_charts.make_pie_chart(labels, values, titles[request.form["pie_data"]] + " per " + titles[request.form["pie_divisions"]])

        return render_template(
            'graphs.html',
            graph_type=request.form['type'],
            plt_graph=plt_graph
        )

@app.route('/graphs/advanced')
def graphs_advanced():
        return render_template(
            'graphs.html',
            advanced=True
        )

# Set debug=True for the server to auto-reload when there are changes
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

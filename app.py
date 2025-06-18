#!/usr/bin/python3
import importlib
from flask import Flask, render_template, request, jsonify
from api.v1 import api_routes
from data import storage
from errors import errors
from crud.colour_identity import Colour_Identity_crud
from crud.deck import deck_crud
from crud.game import Game_crud
from crud.player import Player_crud
from crud.seat import Seat_crud
from graphs import pie_charts, xy_graphs
from utils import utils

app = Flask(__name__)
app.register_blueprint(api_routes)

#################
# Regular pages #
#################
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
        if input_type == "deck":
            call_error = False
            missing_entries = []

            owner_name = request.form["owner"]
            owner_data = storage.get(class_name="Player", key="player_name", value=owner_name)
            if not owner_data:
                call_error = True
                missing_entries.append(["Player", "player_name", owner_name])

            colour_identity_data, desired_ci = utils.get_ci_data_from_dropdown_inputs(request.form)
            if not colour_identity_data:
                call_error = True
                missing_entries.append(["Colour_Identity", "colours", desired_ci])

            if call_error:
                return errors.entry_not_found('input.html', missing_entries, 'create')

            new_deck = {
                "deck_name": request.form["deck_name"],
                "player_id": owner_data[0].id,
                "colour_identity_id": colour_identity_data[0].id
                }

            deck_crud.create(data=jsonify(new_deck))
        elif input_type == "game":
            # get the data needed to create a new Game
            new_game = {
                "start_time": request.form["start_time"],
                "end_time": request.form["end_time"],
            }

            # create the new Game
            new_game_object = Game_crud.create(data=jsonify(new_game))

            # get the data needed to create new Seats
            game_decks = request.form.getlist("game_decks")
            game_players = request.form.getlist("game_players")
            game_ko_turns = request.form.getlist("game_ko_turns")

            # make sure each seat has a deck, player, and ko_turn
            if (len(game_decks) != len(game_players)) or (len(game_decks) != len(game_ko_turns)):
                raise ValueError("Error: a Game must have the same number of decks, players, and ko turns")

            # loop over number of seats
            for i in range(len(game_decks)):
                # find the deck and player id, and ko_turn, for each seat
                desired_deck = deck_crud.specific(key="deck_name", value=game_decks[i])
                desired_player = Player_crud.specific(key="player_name", value=game_players[i])
                if game_ko_turns[i]:
                    ko_turn = int(game_ko_turns[i])
                else:
                    ko_turn = None

                new_seat = {
                    "seat_no": i + 1,
                    "ko_turn": ko_turn,
                    "deck_id": desired_deck["id"],
                    "game_id": new_game_object["id"],
                    "player_id": desired_player["id"]
                }

                # create the new seat
                Seat_crud.create(data=jsonify(new_seat))

            # update the game name, game length in time, game length in turns, and game winner
            # these were left empty because they are derived quantities, so it's easiet to wait until all inputs were added to the database
            Game_crud.update_game_name(new_game_object["id"])
            Game_crud.update_game_time(new_game_object["id"])
            Game_crud.update_game_turns(new_game_object["id"])
            Game_crud.update_game_winner(new_game_object["id"])
        elif input_type == "player":
            new_player = {
                "player_name": request.form["player_name"]
            }

            Player_crud.create(data=jsonify(new_player))

    # Then load the data we need
    colour_identities = Colour_Identity_crud.all(True)
    decks = deck_crud.all(True)
    players = Player_crud.all(True)

    # Prepare data to pass to the template
    html_data = {"colour_identities": colour_identities,
                 "decks": decks,
                 "players": players}

    return render_template('input.html', method="create", data=html_data)

@app.route('/input/edit', methods=['GET', 'POST'])
def input_edit():
    """ Data is edited here """
    if request.method == 'POST':
        # First add the new item to the database
        input_type = request.form["type"]

        # this desperately wants to be a select case, but I'm using Python 3.8 :(
        if input_type == "deck":
            try:
                deck_to_edit = deck_crud.specific('deck_name', request.form['deck_name'])
            except:
                return errors.entry_not_found('input.html', [['deck', 'deck_name', request.form['deck_name']]], 'edit')

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
            if request.form.getlist("ci_abbr"):
                colour_identity_data, desired_ci = utils.get_ci_data_from_dropdown_inputs(request.form)
                if colour_identity_data:
                    new_deck_data.update({
                        "colour_identity_id": colour_identity_data[0].id
                    })
                else:
                    call_error = True
                    missing_entries.append(["Colour_Identity", "colours", desired_ci])

            if call_error:
                return errors.entry_not_found('input.html', missing_entries, 'edit')

            deck_crud.update(deck_to_edit["id"], jsonify(new_deck_data))
        elif input_type == "game":
            try:
                game_to_edit = Game_crud.specific('game_name', request.form['game_name'])
            except:
                return errors.entry_not_found('input.html', [['Game', 'game_name', request.form['game_name']]], 'edit')

            new_game_data = {}
            if request.form["new_start_time"]:
                new_game_data.update({
                    "start_time": request.form["new_start_time"]
                })
            if request.form["new_end_time"]:
                new_game_data.update({
                    "end_time": request.form["new_end_time"]
                })

            Game_crud.update(game_to_edit["id"], jsonify(new_game_data))

            # logic on updating seats goes here

            Game_crud.update_game_name(game_to_edit["id"])
            Game_crud.update_game_time(game_to_edit["id"])
        elif input_type == "player":
            try:
                player_to_edit = Player_crud.specific('player_name', request.form['player_name'])
            except:
                return errors.entry_not_found('input.html', [['Player', 'player_name', request.form['player_name']]], 'edit')

            new_player_data = {}
            if request.form["new_player_name"]:
                new_player_data.update({
                    "player_name": request.form["new_player_name"]
                })

            Player_crud.update(player_to_edit["id"], jsonify(new_player_data))

    # Then load all the database data to pass to the template
    html_data = utils.load_all_db_data()

    return render_template('input.html', method="edit", data=html_data)

@app.route('/input/delete', methods=['GET', 'POST'])
def input_delete():
    """ Data is deleted here """
    if request.method == 'POST':
        # This dict maps an input, taken from the dropdown menu, to the relevant crud class
        module_names = {
            "deck": deck_crud,
            "game": Game_crud,
            "player": Player_crud
        }

        # Find the type of data to delete
        input_type = request.form["type"]

        # Find the specific entry to delete, and either delete it or return an error
        try:
            entry_to_delete = module_names[input_type].specific("%s_name" % input_type,
                                                                request.form["%s_name" % input_type])
        except:
            return errors.entry_not_found('input.html',
                                          [[input_type, "%s_name" % input_type, request.form["%s_name" % input_type]]],
                                          'delete')
        module_names[input_type].delete(entry_to_delete['id'])

    # Load the data we need
    decks = deck_crud.all(True)
    games = Game_crud.all(True)
    players = Player_crud.all(True)

    # Prepare data to pass to the template
    html_data = {"decks": decks,
                 "games": games,
                 "players": players}

    return render_template('input.html', method="delete", data=html_data)

@app.route('/data', methods=['GET'])
def data_get():
    """ Spreadsheets are called here """
    # Load the data we need
    colour_identities = Colour_Identity_crud.all(True)
    players = Player_crud.all(True)

    # Prepare data to pass to the template
    html_data = {"colour_identities": colour_identities,
                 "players": players}

    return render_template('data.html', data=html_data)

@app.route('/data', methods=['POST'])
def data_post():
    """ Spreadsheets are displayed here """
    # Load the data we need
    colour_identities = Colour_Identity_crud.all(True)
    players = Player_crud.all(True)

    # this desperately wants to be a select case, but I'm using Python 3.8 :(
    if request.form["type"] == "colour_identity":
        colour_identity_data = [
            [{
                "ci_name": "0 colours",
                "colours": "skip",
                "number_of_decks": 0
            }],
            [{
                "ci_name": "1 colour",
                "colours": "skip",
                "number_of_decks": 0
            }],
            [{
                "ci_name": "2 colours",
                "colours": "skip",
                "number_of_decks": 0
            }],
            [{
                "ci_name": "3 colours",
                "colours": "skip",
                "number_of_decks": 0
            }],
            [{
                "ci_name": "4 colours",
                "colours": "skip",
                "number_of_decks": 0
            }],
            [{
                "ci_name": "5 colours",
                "colours": "skip",
                "number_of_decks": 0
            }]
        ]

        # if we have a restriction on the player name
        if request.form['player_name']:
            # check that player exists in database, return an error if it doesn't
            player_name = request.form["player_name"]
            player_data = storage.get(class_name="Player", key="player_name", value=player_name)
            if not player_data:
                return errors.entry_not_found('data.html', [["Player", "player_name", player_name]])

            # loop over all colour identities
            for colour_identity in colour_identities:
                # find all decks of with the given colour identity
                colour_identity_decks = Colour_Identity_crud.get_child_data(colour_identity.id, "deck", True)
                decks_to_remove = []

                # loop over those decks
                for deck in colour_identity_decks:
                    # if they have the wrong owner, add them of the list of decks to remove
                    if deck.player.player_name != request.form['player_name']:
                        decks_to_remove.append(deck)

                # loop over our list of decks to remove and remove them from our list of all decks
                for deck_to_remove in decks_to_remove:
                    colour_identity_decks.remove(deck_to_remove)

                # find the number of decks of the given colour identity
                num_decks = len(colour_identity_decks)

                # find the number of colours of the given colour identity
                num_colours = colour_identity.num_colours

                # add all the relevant data that has been requested
                colour_identity_data[num_colours][0]["number_of_decks"] += num_decks
                colour_identity_data[num_colours].append({
                    "ci_name": colour_identity.ci_name,
                    "colours": colour_identity.colours,
                    "number_of_decks": num_decks,
                    "num_colours": num_colours
                })
        else:
            for colour_identity in colour_identities:
                # if we have no restriction the number of decks is just the length of the array
                num_decks = len(Colour_Identity_crud.get_child_data(colour_identity.id, "deck", True))

                # find the number of colours of the given colour identity
                num_colours = colour_identity.num_colours

                # add all the relevant data that has been requested
                colour_identity_data[num_colours][0]["number_of_decks"] += num_decks
                colour_identity_data[num_colours].append({
                    "ci_name": colour_identity.ci_name,
                    "colours": colour_identity.colours,
                    "number_of_decks": num_decks,
                    "num_colours": num_colours
                })

        # Prepare data to pass to the template
        html_data = {"colour_identities": colour_identity_data,
                     "players": players}

        return render_template('data.html', data_type="colour_identity", data=html_data)
    elif request.form["type"] == "deck":
        decks = deck_crud.all(True)
        restrictions = []

        for form_item in request.form:
            if form_item != "type" and request.form[form_item]:
                restriction_key = form_item
                restriction_value = request.form[form_item]

                # this wants to be a select case, but I'm using Python 3.8 :(
                if form_item == "player_name":
                    # check that player exists in database, return an error if it doesn't
                    player_data = storage.get(class_name="Player", key="player_name", value=restriction_value)
                    if not player_data:
                        return errors.entry_not_found('data.html', [["Player", "player_name", restriction_value]])

                    class_type = "Player"

                elif form_item == "ci_abbr":
                    colour_identity_data, desired_ci = utils.get_ci_data_from_dropdown_inputs(request.form)
                    if not colour_identity_data:
                        return errors.entry_not_found(["Colour_Identity", "colours", desired_ci])
                    restriction_key = "ci_name"
                    restriction_value = colour_identity_data[0].ci_name

                    class_type = "Colour_Identity"

                restrictions.append({
                    "class_type": class_type,
                    "key": restriction_key,
                    "value": restriction_value
                })

        if restrictions:
            deck_data = decks
            decks_to_remove = []

            for deck in deck_data:
                for restriction in restrictions:
                    parent_data = deck_crud.get_parent_data(deck.id, restriction["class_type"], True)
                    if getattr(parent_data[0], restriction["key"]) != restriction["value"]:
                        decks_to_remove.append(deck)
                        break

            for deck_to_remove in decks_to_remove:
                deck_data.remove(deck_to_remove)
        else:
            deck_data = decks

        for deck in deck_data:
            deck.games_played = len(deck_crud.get_child_data(deck.id, "Seat", True))

            if deck.games_played == 0:
                deck.win_rate = 0
            else:
                games_won = len(Game_crud.specific("winning_deck_id", deck.id, True))
                deck.win_rate = games_won / deck.games_played * 100

        # Prepare data to pass to the template
        html_data = {"colour_identities": colour_identities,
                     "decks": deck_data,
                     "players": players}

        return render_template('data.html', data_type="deck", data=html_data)
    elif request.form["type"] == "game":
        # Load the data we need
        colour_identities = Colour_Identity_crud.all(True)
        games = Game_crud.all(True)
        players = Player_crud.all(True)
        num_seats = 0

        for game in games:
            seats = Game_crud.get_child_data(game.id, "Seat", True)
            game.player = [None] * len(seats)
            game.deck = [None] * len(seats)

            game.winner = game.winning_player.player_name + " - " + game.winning_deck.deck_name

            for seat in seats:
                game.player[seat.seat_no - 1] = seat.player
                game.deck[seat.seat_no - 1] = seat.deck

            if len(seats) > num_seats:
                num_seats = len(seats)

        # Prepare data to pass to the template
        html_data = {"colour_identities": colour_identities,
                     "games": games,
                     "players": players,
                     "num_seats": num_seats}

        return render_template('data.html', data_type="game", data=html_data)
    elif request.form["type"] == "player":
        player_data = []

        # if we have a restriction on the colour identity name
        if request.form.getlist("ci_abbr"):
            colour_identity_data, desired_ci = utils.get_ci_data_from_dropdown_inputs(request.form)
            ci_name = colour_identity_data[0].ci_name

            # loop over all players
            for player in players:
                # find all decks owned by a given player
                player_decks = Player_crud.get_child_data(player.id, "deck", True)
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
                    "id": player.id,
                    "player_name": player.player_name,
                    "number_of_decks": num_decks
                })
        else:
            for player in players:
                # if we have no restriction the number of decks is just the length of the array
                num_decks = len(Player_crud.get_child_data(player.id, "deck", True))

                player_data.append({
                    "id": player.id,
                    "player_name": player.player_name,
                    "number_of_decks": num_decks
                })

        # find number of games played and win rate
        # start by looping over all players
        for player in player_data:
            # number of games played is the number of child seats
            player["games_played"] = len(Player_crud.get_child_data(player["id"], "Seat", True))

            # if they've played no games we need to set the win rate manually to avoid divide by zero errors
            if player["games_played"] == 0:
                player["win_rate"] = 0
            else:
                # number of games won is the number of games with winning_player_id equal to the player's id
                games_won = len(Game_crud.specific("winning_player_id", player["id"], True))
                player["win_rate"] = games_won / player["games_played"] * 100

        # Prepare data to pass to the template
        html_data = {"colour_identities": colour_identities,
                     "players": player_data}

        return render_template('data.html', data_type="player", data=html_data)

    # Prepare data to pass to the template
    html_data = {"colour_identities": colour_identities,
                 "players": players}

    return render_template('data.html', data=html_data)

@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    """ Graphs are displayed here """
    # Load the data we need before passing it to the template
    if request.method == 'GET':
        deck_data = deck_crud.all(True)

        plt_data = {}

        for ii in list(range(0,6)):
            plt_data.update({"%s colours" % ii: 0})

        for deck in deck_data:
            deck_num_colours = deck.colour_identity.num_colours
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
        call_error = False
        missing_entries = []

        model_names = {
            "deck": {
                "file": "deck",
                "class": "deck_crud",
                "name_column": "deck_name"
            }
        }
        titles = {
            "colour": "Colour",
            "colour identity": "Colour Identity",
            "deck": "Number of Decks",
            "number of colours": "Number of Colours",
            "number of decks": "Number of Decks",
            "owner": "Player",
            "win rate": "Win Rate"
        }

        if request.form['type'] == "bar":
            if request.form["bar_data"] not in list(model_names.keys()):
                call_error = True
                missing_entries.append([request.form["bar_data"], 'Data Type'])
                return errors.option_not_available('graphs.html', missing_entries)

            xy_data = {}

            if "no_zeroes" in request.form:
                no_zeroes = True
            else:
                no_zeroes = False

            crud_file = importlib.import_module("crud." + model_names[request.form["bar_data"]]["file"])
            crud_class = getattr(crud_file, model_names[request.form["bar_data"]]["class"])
            data = crud_class.all(True)

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
                        if "c" in datum_colours:
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
                    call_error = True
                    missing_entries.append([request.form["bar_y"], 'Y axis'])
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
                    call_error = True
                    missing_entries.append([request.form["bar_y"], 'Y axis'])
            elif request.form["bar_x"] == "number of colours":
                for ii in list(range(0,6)):
                    xy_data.update({"%s colours" % ii: 0})

                if request.form["bar_y"] == "number of decks":
                    for datum in data:
                        datum_num_colours = datum.colour_identity.num_colours
                        xy_data["%s colours" % datum_num_colours] += 1
                else:
                    call_error = True
                    missing_entries.append([request.form["bar_y"], 'Y axis'])
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
                elif request.form["bar_y"] == "win rate":
                    for datum in data:
                        datum_player_model = getattr(datum, "player")
                        datum_owner = getattr(datum_player_model, "player_name")
                        games_played = len(Player_crud.get_child_data(getattr(datum_player_model, "id"), "Seat", True))

                        if games_played == 0:
                            xy_data[datum_owner] = 0
                        else:
                            games_won = len(Game_crud.specific("winning_player_id", getattr(datum_player_model, "id"), True))
                            xy_data[datum_owner] = games_won/games_played * 100
                else:
                    call_error = True
                    missing_entries.append([request.form["bar_y"], 'Y axis'])
            elif request.form["bar_x"] == "deck":
                decks = deck_crud.all(True)

                for deck in decks:
                    deck_name = getattr(deck, "deck_name")
                    xy_data.update({deck_name: 0})

                if request.form["bar_y"] == "win rate":
                    for datum in data:
                        datum_name = getattr(datum, "deck_name")
                        games_played = len(deck_crud.get_child_data(getattr(datum, "id"), "Seat", True))

                        if games_played == 0:
                            xy_data[datum_name] = 0
                        else:
                            games_won = len(Game_crud.specific("winning_deck_id", getattr(datum, "id"), True))
                            xy_data[datum_name] = games_won/games_played * 100
            else:
                call_error = True
                missing_entries.append([request.form["bar_x"], 'X axis'])

            if call_error:
                return errors.option_not_available('graphs.html', missing_entries)

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
                call_error = True
                missing_entries.append([request.form["pie_data"], 'Data Type'])
                return errors.option_not_available('graphs.html', missing_entries)

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
                    if "c" in datum_colours:
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
                    datum_num_colours = datum.colour_identity.num_colours
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
                call_error = True
                missing_entries.append([request.form["pie_divisions"], 'Slices'])

            if call_error:
                return errors.option_not_available('graphs.html', missing_entries)

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

###############
# Error pages #
###############
@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')

# Set debug=True for the server to auto-reload when there are changes
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

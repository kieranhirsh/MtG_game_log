import importlib
import time
from collections import defaultdict
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
import requests
from api.v1 import api_routes
from data import storage
from errors import errors
from crud.colour_identity import colour_identity_crud
from crud.deck import deck_crud
from crud.game import game_crud
from crud.player import player_crud
from crud.seat import seat_crud
from graphs import bar_charts, line_graphs, pie_charts
from utils import curl_utils, derived_quantities, utils

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
def input_add():
    """ Data is inputted here """
    if request.method == 'POST':
        # First add the new item to the database
        input_type = request.form["type"]

        # this desperately wants to be a select case, but I'm using Python 3.8 :(
        if input_type == "deck":
            # initialise some values
            call_error = False
            missing_entries = []

            # get the owner id
            owner_name = request.form["owner"]
            owner_data = storage.get(class_name="player", key="player_name", value=owner_name)
            if not owner_data:
                call_error = True
                missing_entries.append(["player", "player_name", owner_name])

            # get commander id
            commander_name = request.form["deck_commander_1"]
            response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={commander_name}").json()
            if "status" in response:
                return errors.card_not_found('input.html', [response["details"]], 'create')
            commander_name = response["name"]
            commander_colours = response["color_identity"]

            # get partner/background id
            if request.form["deck_commander_2"]:
                partner_name = request.form["deck_commander_2"]
                response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={partner_name}").json()
                if "status" in response:
                    return errors.card_not_found('input.html', [response["details"]], 'create')
                partner_name = response["name"]
                partner_colours = response["color_identity"]
            else:
                partner_name = ""
                partner_colours = []

            # get edhrec data
            edhrec_uri = curl_utils.get_edhrec_uri_from_commander_names([commander_name, partner_name])
            edhrec_num_decks, edhrec_popularity = curl_utils.get_popularity_from_edhrec_uri(edhrec_uri)

            # get companion id
            if request.form["deck_companion"]:
                companion_name = request.form["deck_companion"]
                response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={companion_name}").json()
                if "status" in response:
                    return errors.card_not_found('input.html', [response["details"]], 'create')
                companion_name = response["name"]
            else:
                companion_name = ""

            # get the deck name
            if request.form["deck_name"]:
                deck_name = request.form['deck_name']
            else:
                deck_name = commander_name
                if partner_name:
                    deck_name += f" / {partner_name}"
                if companion_name:
                    deck_name += f" + {companion_name}"

            # get the colour identity id
            colour_identity_data, _ = utils.get_ci_data_from_list_of_colours(request.form.getlist("ci_abbr"))
            if not colour_identity_data:
                deck_colours = commander_colours + partner_colours
                deck_colours = [colour.lower() for colour in deck_colours]
                colour_identity_data, desired_ci = utils.get_ci_data_from_list_of_colours(deck_colours)
                if not colour_identity_data:
                    call_error = True
                    missing_entries.append(["colour_identity", "colours", desired_ci])

            if call_error:
                return errors.entry_not_found('input.html', missing_entries, 'create')

            new_deck = {
                "deck_name": deck_name,
                "commander_name": commander_name,
                "partner_name": partner_name,
                "companion_name": companion_name,
                "player_id": owner_data[0].id,
                "edhrec_num_decks": edhrec_num_decks,
                "edhrec_popularity": edhrec_popularity,
                "last_accessed": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "colour_identity_id": colour_identity_data[0].id
                }

            deck_crud.create(data=jsonify(new_deck))
        elif input_type == "game":
            # get the data needed to create a new game
            new_game = {
                "start_time": request.form["start_time"],
                "end_time": request.form["end_time"],
            }

            # create the new game
            new_game_object = game_crud.create(data=jsonify(new_game))

            # get the data needed to create new seats
            game_decks = request.form.getlist("game_decks")
            game_players = request.form.getlist("game_players")
            game_ko_turns = request.form.getlist("game_ko_turns")

            # make sure each seat has a deck, player, and ko_turn
            if (len(game_decks) != len(game_players)) or (len(game_decks) != len(game_ko_turns)):
                raise ValueError("Error: a game must have the same number of decks, players, and ko turns")

            # loop over number of seats
            for i in range(len(game_decks)):
                # find the deck and player id, and ko_turn, for each seat
                deck_name, _, query_tree = utils.get_deck_data_from_form_inputs(game_decks[i])
                try:
                    desired_deck = deck_crud.specific(query_tree=query_tree, join_classes=["player"])
                except:
                    return errors.entry_not_found('input.html', [['deck', 'deck_name', deck_name]], 'edit')
                desired_player = player_crud.specific(key="player_name", value=game_players[i])
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
                seat_crud.create(data=jsonify(new_seat))

            # update the game name, game length in turns, and game winner
            # these were left empty because they are derived quantities
            # so it's easiet to wait until all inputs were added to the database
            # but really they want to be removed from the db completely
            game_crud.update_game_name(new_game_object["id"])
        elif input_type == "player":
            new_player = {
                "player_name": request.form["player_name"]
            }

            player_crud.create(data=jsonify(new_player))

    # Then load the data we need
    colour_identities = colour_identity_crud.all(True)
    decks = deck_crud.all(True)
    players = player_crud.all(True)

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
            deck_name, _, query_tree = utils.get_deck_data_from_form_inputs(request.form['requested_deck'])
            try:
                deck_to_edit = deck_crud.specific(query_tree=query_tree, join_classes=["player"])
            except:
                return errors.entry_not_found('input.html', [['deck', 'deck_name', deck_name]], 'edit')

            new_deck_data = {}
            call_error = False
            missing_entries = []

            # get deck name
            if request.form["new_deck_name"]:
                new_deck_data.update({
                    "deck_name": request.form["new_deck_name"]
                })

            # get commander name
            if request.form["new_deck_commander_1"]:
                commander_name = request.form["new_deck_commander_1"]
                response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={commander_name}").json()
                if "status" in response:
                    return errors.card_not_found('input.html', [response["details"]], 'create')
                commander_name = response["name"]
                new_deck_data.update({
                    "commander_name": commander_name
                })

            # get partner/background name
            if request.form["new_deck_commander_2"]:
                partner_name = request.form["new_deck_commander_2"]
                response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={partner_name}").json()
                if "status" in response:
                    return errors.card_not_found('input.html', [response["details"]], 'create')
                partner_name = response["name"]
                new_deck_data.update({
                    "partner_name": partner_name
                })

            # get companion name
            if request.form["new_deck_companion"]:
                companion_name = request.form["new_deck_companion"]
                response = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={companion_name}").json()
                if "status" in response:
                    return errors.card_not_found('input.html', [response["details"]], 'create')
                companion_name = response["name"]
                new_deck_data.update({
                    "companion_name": companion_name
                })

            # get owner id
            if request.form["new_owner"]:
                owner_name = request.form["new_owner"]
                owner_data = storage.get(class_name="player", key="player_name", value=owner_name)

                if owner_data:
                    new_deck_data.update({
                        "player_id": owner_data[0].id
                    })
                else:
                    call_error = True
                    missing_entries.append(["player", "player_name", owner_name])

            # get colour identity id
            if request.form.getlist("ci_abbr"):
                colour_identity_data, desired_ci = utils.get_ci_data_from_list_of_colours(request.form.getlist("ci_abbr"))
                if colour_identity_data:
                    new_deck_data.update({
                        "colour_identity_id": colour_identity_data[0].id
                    })
                else:
                    call_error = True
                    missing_entries.append(["colour_identity", "colours", desired_ci])

            if call_error:
                return errors.entry_not_found('input.html', missing_entries, 'edit')

            deck_crud.update(deck_to_edit["id"], jsonify(new_deck_data))
        elif input_type == "game":
            game_decks = request.form.getlist("game_decks")
            game_players = request.form.getlist("game_players")
            game_ko_turns = request.form.getlist("game_ko_turns")

            try:
                game_to_edit = game_crud.specific('game_name', request.form['game_name'])
            except:
                return errors.entry_not_found('input.html', [['game', 'game_name', request.form['game_name']]], 'edit')

            new_game_data = {}
            if request.form["new_start_time"]:
                new_game_data.update({
                    "start_time": request.form["new_start_time"]
                })
            if request.form["new_end_time"]:
                new_game_data.update({
                    "end_time": request.form["new_end_time"]
                })

            game_crud.update(game_to_edit["id"], jsonify(new_game_data))

            seats = seat_crud.specific(key="game_id", value=game_to_edit["id"])
            for seat_to_edit in seats:
                seat_no = seat_to_edit["seat_no"] - 1

                if game_decks[seat_no] or game_players[seat_no] or game_ko_turns[seat_no]:
                    deck_name, _, query_tree = utils.get_deck_data_from_form_inputs(game_decks[seat_no])
                    deck_id = deck_crud.specific(query_tree=query_tree, join_classes=['player'])['id']

                    player_id = player_crud.specific(key='player_name', value=game_players[seat_no])['id']

                    if game_ko_turns[seat_no]:
                        ko_turn = int(game_ko_turns[seat_no])
                    else:
                        ko_turn = None

                    new_seat_data = {
                        "deck_id": deck_id,
                        "player_id": player_id,
                        "ko_turn": ko_turn
                    }

                    seat_crud.update(seat_to_edit["id"], jsonify(new_seat_data))

            game_crud.update_game_name(game_to_edit["id"])
        elif input_type == "player":
            try:
                player_to_edit = player_crud.specific('player_name', request.form['player_name'])
            except:
                return errors.entry_not_found('input.html',
                                              [['player', 'player_name', request.form['player_name']]],
                                              'edit')

            new_player_data = {}
            if request.form["new_player_name"]:
                new_player_data.update({
                    "player_name": request.form["new_player_name"]
                })

            player_crud.update(player_to_edit["id"], jsonify(new_player_data))

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
            "game": game_crud,
            "player": player_crud
        }

        # Find the type of data to delete
        input_type = request.form["type"]

        if input_type == "deck":
            deck_name, _, query_tree = utils.get_deck_data_from_form_inputs(request.form['requested_deck'])
            try:
                deck_to_delete = deck_crud.specific(query_tree=query_tree, join_classes=["player"])
            except:
                return errors.entry_not_found('input.html', [['deck', 'deck_name', deck_name]], 'delete')

            deck_crud.delete(deck_to_delete['id'])
        else:
            # Find the specific entry to delete, and either delete it or return an error
            try:
                entry_to_delete = module_names[input_type].specific(f"{input_type}_name",
                                                                    request.form[f"{input_type}_name"])
            except:
                return errors.entry_not_found('input.html',
                                              [[input_type, f"{input_type}_name",
                                                request.form[f"{input_type}_name"]]],
                                              'delete')
            module_names[input_type].delete(entry_to_delete['id'])

    # Load the data we need
    decks = deck_crud.all(True)
    games = game_crud.all(True)
    players = player_crud.all(True)

    # Prepare data to pass to the template
    html_data = {"decks": decks,
                 "games": games,
                 "players": players}

    return render_template('input.html', method="delete", data=html_data)

@app.route('/data', methods=['GET'])
def data_get():
    """ Spreadsheets are called here """
    # Load the data we need
    colour_identities = colour_identity_crud.all(True)
    decks = deck_crud.all(True)
    players = player_crud.all(True)

    # Prepare data to pass to the template
    html_data = {"colour_identities": colour_identities,
                 "decks": decks,
                 "players": players}

    return render_template('data.html', menu_data=html_data)

@app.route('/data', methods=['POST'])
def data_post():
    """ Spreadsheets are displayed here """
    # Load the data we need
    colour_identities = colour_identity_crud.all(True)
    decks = deck_crud.all(True)
    players = player_crud.all(True)
    html_data = {"colour_identities": colour_identities.copy(),
                 "decks": decks.copy(),
                 "players": players.copy()}

    # this desperately wants to be a select case, but I'm using Python 3.8 :(
    if request.form["type"] == "colour_identity":
        # initialise values
        colour_identity_data = []
        for i in range(6):
            if i == 1:
                colours = "colour"
            else:
                colours = "colours"
            colour_identity_data.append(
                [{
                    "ci_name": f"{i} {colours}",
                    "colours": "skip",
                    "number_of_decks": 0,
                    "games_played": 0,
                    "games_won": 0,
                    "win_rate": 0,
                    "time_played": 0,
                    "timed_games": 0,
                    "turns_played": 0,
                    "turned_games": 0,
                    "total_ko_turns": 0,
                    "num_ko_games": 0,
                    "ave_game_time": 0,
                    "ave_game_turns": 0,
                    "ave_first_ko": 0,
                    "ave_edhrec_decks": 0,
                    "ave_edhrec_ranking": 0,
                    "num_edhrec_data": 0,
                    "total_edhrec_decks": 0
                }])

        # generate the full list of edhrec deck data
        min_edhrec_decks = min([deck.edhrec_num_decks for deck in decks if isinstance(deck.edhrec_num_decks, int)])
        page = 1
        edhrec_all_cmdrs_response = requests.get("https://json.edhrec.com/pages/commanders/year.json").json()
        popularity_list = edhrec_all_cmdrs_response["container"]["json_dict"]["cardlists"][0]["cardviews"]
        while popularity_list[-1]["num_decks"] > min_edhrec_decks:
            edhrec_all_cmdrs_response = requests.get(f"https://json.edhrec.com/pages/commanders/year-past2years-{page}.json").json()
            popularity_list += edhrec_all_cmdrs_response["cardviews"]
            page += 1

        # loop over all colour identities
        for colour_identity in colour_identities:
            # find all decks of with the given colour identity
            colour_identity_decks = colour_identity_crud.get_child_data(colour_identity.id, "deck", True)
            decks_to_remove = []

            # if we have a restriction on the player name
            if request.form['player_name']:
                # check that player exists in database, return an error if it doesn't
                player_name = request.form["player_name"]
                player_data = storage.get(class_name="player", key="player_name", value=player_name)
                if not player_data:
                    return errors.entry_not_found('data.html', [["player", "player_name", player_name]])

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

            # initialise some values
            num_games_played = 0
            num_games_won = 0
            time_played = 0
            timed_games = 0
            turns_played = 0
            turned_games = 0
            sum_first_kos = 0
            len_first_kos = 0
            num_edhrec_deck = []
            # find the number of games played and win rate
            for deck in colour_identity_decks:
                # initialise some values
                game_times = []
                game_turns = []
                first_kos = []

                # find the edhrec data for each relevant deck player owns
                if deck.edhrec_num_decks:
                    num_edhrec_deck.append(deck.edhrec_num_decks)

                # find all games played by the deck
                for seat in deck_crud.get_child_data(deck.id, "seat", True):
                    # get the time taken for each of those games
                    _, game_seconds = derived_quantities.game_length_in_time(seat.game)
                    if game_seconds:
                        game_times.append(game_seconds)
                    # get the length in turns for each of those games
                    game_length = derived_quantities.game_length_in_turns(seat.game)
                    if game_length:
                        game_turns.append(game_length)
                    # get the first turn a player was KO'd for each of those games
                    first_ko = derived_quantities.game_first_ko(seat.game)
                    if first_ko:
                        first_kos.append(first_ko)

                # add the total time and number of timed games to the running tally
                time_played += sum(game_times)
                timed_games += len(game_times)
                turns_played += sum(game_turns)
                turned_games += len(game_turns)
                sum_first_kos += sum(first_kos)
                len_first_kos += len(first_kos)

                # find all the games this deck has played
                deck_seats = deck_crud.get_child_data(deck.id, "seat", True)
                num_games_played += len(deck_seats)
                # loop over the number of games played and count the number of games won
                for seat in deck_seats:
                    _, winning_deck = derived_quantities.game_winning_player_and_deck(seat.game)
                    if winning_deck.id == deck.id:
                        num_games_won += 1

            # if they've played no games we need to set the win rate manually to avoid divide by zero errors
            if num_games_played == 0:
                win_rate = 0
            else:
                win_rate = num_games_won / num_games_played * 100

            # same goes for timed games
            if timed_games == 0:
                ave_game_time = ""
            else:
                ave_time = time_played / timed_games
                ave_game_time = str(timedelta(seconds=(ave_time - (ave_time % 60))))[:-3]

            # and average game length
            if turned_games == 0:
                ave_game_turns = ""
            else:
                ave_game_turns = turns_played / turned_games
                ave_game_turns = f"{ave_game_turns:.1f}"

            # and average first_ko
            if len_first_kos == 0:
                ave_first_ko = ""
            else:
                ave_first_ko = sum_first_kos / len_first_kos
                ave_first_ko = f"{ave_first_ko:.1f}"

            # if there's no edhrec data we need to set the average number of
            # decks manually to avoid divide by zero errors
            if len(num_edhrec_deck) == 0:
                ave_edhrec_decks = 0
                ave_edhrec_ranking = ""
            else:
                # these lines are here because of a really annoying bug to track where sometimes
                # the line that calculates ave_edhrec_decks fails due to unsopported comparison types
                print(colour_identity.ci_name)
                print(num_edhrec_deck)
                ave_edhrec_decks = sum(num_edhrec_deck) / len(num_edhrec_deck)
                # find the ranking that the player's average deck would have on EDHrec
                rank = 0
                while ave_edhrec_decks < popularity_list[rank]["num_decks"]:
                    rank += 1
                ave_edhrec_ranking = f"#{rank + 1} ({popularity_list[rank]['name']})"

            # find the number of colours of the given colour identity
            num_colours = colour_identity.num_colours

            # add all the relevant data that has been requested
            # this handles the data binned by number of colours
            colour_identity_data[num_colours][0]["number_of_decks"] += num_decks
            colour_identity_data[num_colours][0]["games_played"] += num_games_played
            colour_identity_data[num_colours][0]["games_won"] += num_games_won
            if colour_identity_data[num_colours][0]["games_played"] == 0:
                colour_identity_data[num_colours][0]["win_rate"] = 0
            else:
                colour_identity_data[num_colours][0]["win_rate"] = (colour_identity_data[num_colours][0]["games_won"]
                                                                    / colour_identity_data[num_colours][0]["games_played"]
                                                                    * 100)
            colour_identity_data[num_colours][0]["timed_games"] += timed_games
            colour_identity_data[num_colours][0]["time_played"] += time_played
            if colour_identity_data[num_colours][0]["timed_games"] == 0:
                colour_identity_data[num_colours][0]["ave_game_time"] = ""
            else:
                running_ave_game_time = (colour_identity_data[num_colours][0]["time_played"]
                                         / colour_identity_data[num_colours][0]["timed_games"])
                colour_identity_data[num_colours][0]["ave_game_time"] = str(timedelta(seconds=(running_ave_game_time - (running_ave_game_time % 60))))[:-3]
            colour_identity_data[num_colours][0]["turns_played"] += turns_played
            colour_identity_data[num_colours][0]["turned_games"] += turned_games
            if colour_identity_data[num_colours][0]["turned_games"] == 0:
                colour_identity_data[num_colours][0]["ave_game_turns"] = ""
            else:
                running_ave_game_turns = (colour_identity_data[num_colours][0]["turns_played"]
                                          / colour_identity_data[num_colours][0]["turned_games"])
                colour_identity_data[num_colours][0]["ave_game_turns"] = f"{running_ave_game_turns:.1f}"
            colour_identity_data[num_colours][0]["total_ko_turns"] += sum_first_kos
            colour_identity_data[num_colours][0]["num_ko_games"] += len_first_kos
            if colour_identity_data[num_colours][0]["num_ko_games"] == 0:
                colour_identity_data[num_colours][0]["ave_first_ko"] = ""
            else:
                running_first_ko = (colour_identity_data[num_colours][0]["total_ko_turns"]
                                          / colour_identity_data[num_colours][0]["num_ko_games"])
                colour_identity_data[num_colours][0]["ave_first_ko"] = f"{running_first_ko:.1f}"
            colour_identity_data[num_colours][0]["num_edhrec_data"] += len(num_edhrec_deck)
            colour_identity_data[num_colours][0]["total_edhrec_decks"] += sum(num_edhrec_deck)
            if colour_identity_data[num_colours][0]["num_edhrec_data"] == 0:
                colour_identity_data[num_colours][0]["ave_edhrec_decks"] = ""
                colour_identity_data[num_colours][0]["ave_edhrec_ranking"] = ""
            else:
                running_ave_edhrec_decks = (colour_identity_data[num_colours][0]["total_edhrec_decks"]
                                          / colour_identity_data[num_colours][0]["num_edhrec_data"])
                colour_identity_data[num_colours][0]["ave_edhrec_decks"] = running_ave_edhrec_decks
                # find the ranking that the player's average deck would have on EDHrec
                rank = 0
                while colour_identity_data[num_colours][0]["ave_edhrec_decks"] < popularity_list[rank]["num_decks"]:
                    rank += 1
                colour_identity_data[num_colours][0]["ave_edhrec_ranking"] = f"#{rank + 1} ({popularity_list[rank]['name']})"

            # this handles the data for the specific colour identity
            colour_identity_data[num_colours].append({
                "ci_name": colour_identity.ci_name,
                "colours": colour_identity.colours,
                "number_of_decks": num_decks,
                "num_colours": num_colours,
                "games_played": num_games_played,
                "games_won": num_games_won,
                "win_rate": win_rate,
                "ave_game_time": ave_game_time,
                "ave_game_turns": ave_game_turns,
                "ave_first_ko": ave_first_ko,
                "ave_edhrec_decks": ave_edhrec_decks,
                "ave_edhrec_ranking": ave_edhrec_ranking
            })

        # Prepare data to pass to the template
        html_data = {"colour_identities": colour_identity_data,
                     "decks": decks,
                     "players": players}

        return render_template('data.html', data_type="colour_identity", menu_data=html_data)
    elif request.form["type"] == "deck":
        restrictions = []

        for form_item in request.form:
            if form_item != "type" and form_item != "bins" and request.form[form_item]:
                restriction_key = form_item
                restriction_value = request.form[form_item]

                # this wants to be a select case, but I'm using Python 3.8 :(
                if form_item == "player_name":
                    # check that player exists in database, return an error if it doesn't
                    player_data = storage.get(class_name="player", key="player_name", value=restriction_value)
                    if not player_data:
                        return errors.entry_not_found('data.html', [["player", "player_name", restriction_value]])

                    class_type = "player"

                elif form_item == "ci_abbr":
                    # check that colour identity exists in database, return an error if it doesn't
                    colour_identity_data, desired_ci = utils.get_ci_data_from_list_of_colours(request.form.getlist("ci_abbr"))
                    if not colour_identity_data:
                        return errors.entry_not_found('data.html', [["colour_identity", "colours", desired_ci]])
                    restriction_key = "ci_name"
                    restriction_value = colour_identity_data[0].ci_name

                    class_type = "colour_identity"

                else:
                    return errors.missing_form_item('data.html')

                restrictions.append({
                    "class_type": class_type,
                    "key": restriction_key,
                    "value": restriction_value
                })

        # set up our initial bins
        if "bins" in request.form.keys():
            bin_type = request.form["bins"]
        else:
            bin_type = ""

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

        table_data = {}

        for deck in deck_data:
            # initialise data
            table_data[deck.id] = {"total": defaultdict(int)}
            table_data[deck.id]["total"]["deck_name"] = deck.deck_name
            table_data[deck.id]["total"]["owner_name"] = deck.player.player_name
            table_data[deck.id]["total"]["commander_name"] = deck.commander_name
            table_data[deck.id]["total"]["partner_name"] = deck.partner_name
            table_data[deck.id]["total"]["companion_name"] = deck.companion_name
            table_data[deck.id]["total"]["colour_identity"] = deck.colour_identity.ci_name
            table_data[deck.id]["total"]["colours"] = deck.colour_identity.colours

            # find all the games this deck has played
            deck_seats = deck_crud.get_child_data(deck.id, "seat", True)
            num_games_played = len(deck_seats)
            table_data[deck.id]["total"]["num_games_played"] = num_games_played

            if (not deck.last_accessed
                or ((datetime.now() - datetime.strptime(str(deck.last_accessed), "%Y-%m-%d %H:%M:%S"))
                    > timedelta(hours=5, minutes=59))
               ):
                try:
                    edhrec_uri = curl_utils.get_edhrec_uri_from_commander_names([deck.commander_name,
                                                                                 deck.partner_name])
                    edhrec_decks, popularity = curl_utils.get_popularity_from_edhrec_uri(edhrec_uri)
                    table_data[deck.id]["total"]["edhrec_decks"] = edhrec_decks
                    table_data[deck.id]["total"]["popularity"] = popularity
                    deck_crud.update(deck.id, jsonify({"edhrec_num_decks": edhrec_decks,
                                                        "edhrec_popularity": popularity,
                                                        "last_accessed": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}))
                    time.sleep(0.01)
                except:
                    pass
            else:
                table_data[deck.id]["total"]["edhrec_decks"] = deck.edhrec_num_decks
                table_data[deck.id]["total"]["popularity"] = deck.edhrec_popularity

            if num_games_played == 0:
                # if this deck hasn't played any games it's the trivial case
                table_data[deck.id]["total"]["num_games_won"] = 0
                table_data[deck.id]["total"]["win_rate"] = 0
                table_data[deck.id]["total"]["ave_game_time"] = ""
                table_data[deck.id]["total"]["ave_game_turns"] = ""
                table_data[deck.id]["total"]["ave_first_ko"] = ""
                table_data[deck.id]["total"]["last_played"] = "never"
                table_data[deck.id] = {
                    "total": table_data[deck.id]["total"]
                }
            else:
                most_recent_game = {
                    "total": datetime.min
                }
                for seat in deck_seats:
                    # find the type of bins we want, if any, and set the specific bins we want for this game
                    # this wants to be a select case, but I'm using Python 3.8 :(
                    if bin_type == "opp_player":
                        game_bins = []
                        opponents = seat.game.seats
                        for opponent in opponents:
                            if opponent.id != seat.id:
                                game_bins.append({
                                    "bin_name": opponent.player_id,
                                    "default_data": [
                                        {
                                            "key": "owner_name",
                                            "value": f"vs {opponent.player.player_name}"
                                        }
                                    ]
                                })
                    elif bin_type == "opp_deck":
                        game_bins = []
                        opponents = seat.game.seats
                        for opponent in opponents:
                            if opponent.id != seat.id:
                                game_bins.append({
                                    "bin_name": opponent.deck_id,
                                    "default_data": [
                                        {
                                            "key": "deck_name",
                                            "value": f"vs {opponent.deck.deck_name}"
                                        },
                                        {
                                            "key": "owner_name",
                                            "value": f"{opponent.deck.player.player_name}"
                                        },
                                        {
                                            "key": "colour_identity",
                                            "value": f"{opponent.deck.colour_identity.ci_name}"
                                        },
                                        {
                                            "key": "colours",
                                            "value": f"{opponent.deck.colour_identity.colours}"
                                        },
                                        {
                                            "key": "commander_name",
                                            "value": f"{opponent.deck.commander_name}"
                                        },
                                        {
                                            "key": "partner_name",
                                            "value": f"{opponent.deck.partner_name}"
                                        },
                                        {
                                            "key": "companion_name",
                                            "value": f"{opponent.deck.companion_name}"
                                        },
                                        {
                                            "key": "edhrec_decks",
                                            "value": f"{opponent.deck.edhrec_num_decks}"
                                        },
                                        {
                                            "key": "popularity",
                                            "value": f"{opponent.deck.edhrec_popularity}"
                                        }
                                    ]
                                })
                    elif bin_type == "opp_ci":
                        game_bins = []
                        opponents = seat.game.seats
                        opp_ci    = []
                        for opponent in opponents:
                            if opponent.id != seat.id:
                                if opponent.deck.colour_identity.ci_name not in opp_ci:
                                    game_bins.append({
                                        "bin_name": opponent.deck.colour_identity.ci_name,
                                        "default_data": [
                                            {
                                                "key": "colour_identity",
                                                "value": f"vs {opponent.deck.colour_identity.ci_name}"
                                            },
                                            {
                                                "key": "colours",
                                                "value": f"{opponent.deck.colour_identity.colours}"
                                            }
                                        ]
                                    })
                                    opp_ci.append(opponent.deck.colour_identity.ci_name)
                    elif bin_type == "opp_num_colours":
                        game_bins       = []
                        opponents       = seat.game.seats
                        opp_num_colours = []
                        for opponent in opponents:
                            if opponent.id != seat.id:
                                if len(opponent.deck.colour_identity.colours) not in opp_num_colours:
                                    game_bins.append({
                                        "bin_name": len(opponent.deck.colour_identity.colours),
                                        "default_data": [
                                            {
                                                "key": "colour_identity",
                                                "value": f"vs {len(opponent.deck.colour_identity.colours)} colour decks"
                                            }
                                        ]
                                    })
                                    opp_num_colours.append(len(opponent.deck.colour_identity.colours))
                    elif bin_type == "num_players":
                        num_players = len(seat.game.seats)
                        game_bins = [{
                            "bin_name": num_players,
                            "default_data": [
                                {
                                    "key": "deck_name",
                                    "value": f"{num_players} player games"
                                }
                            ]
                        }]
                    elif bin_type == "seat":
                        game_bins = [{
                            "bin_name": seat.seat_no,
                            "default_data": [
                                {
                                    "key": "deck_name",
                                    "value": f"seat number {seat.seat_no}"
                                }
                            ]
                        }]
                    elif bin_type == "result":
                        _, winning_deck = derived_quantities.game_winning_player_and_deck(seat.game)
                        if winning_deck.id == deck.id:
                            game_bins = [{
                                "bin_name": "win",
                                "default_data": [
                                    {
                                        "key": "deck_name",
                                        "value": "Games Won"
                                    }
                                ]
                            }]
                        else:
                            game_bins = [{
                                "bin_name": "loss",
                                "default_data": [
                                    {
                                        "key": "deck_name",
                                        "value": "Games Lost"
                                    }
                                ]
                            }]
                    elif bin_type == "game_time":
                        _, game_time = derived_quantities.game_length_in_time(seat.game)
                        if game_time:
                            game_minutes = game_time / 60
                            minutes_bin = int(game_minutes - (game_minutes % 10))
                            default_value = f"{minutes_bin} - {minutes_bin + 10} minute games"
                        else:
                            minutes_bin = "untimed"
                            default_value = "untimed games"
                        game_bins = [{
                            "bin_name": minutes_bin,
                            "default_data": [
                                {
                                    "key": "deck_name",
                                    "value": default_value
                                }
                            ]
                        }]
                    elif bin_type == "game_turns":
                        game_length = derived_quantities.game_length_in_turns(seat.game)
                        game_bins = [{
                            "bin_name": game_length,
                            "default_data": [
                                {
                                    "key": "deck_name",
                                    "value": f"{game_length} turn games"
                                }
                            ]
                        }]
                    elif bin_type == "first_KO":
                        KO_turn = derived_quantities.game_first_ko(seat.game)
                        game_bins = [{
                            "bin_name": KO_turn,
                            "default_data": [
                                {
                                    "key": "deck_name",
                                    "value": f"turn {KO_turn} KO"
                                }
                            ]
                        }]
                    elif bin_type == "self_KO":
                        KO_turn = seat.ko_turn
                        if KO_turn:
                            default_value = f"KO'd on turn {KO_turn}"
                        else:
                            KO_turn = "win"
                            default_value = "Won the game"
                        game_bins = [{
                            "bin_name": KO_turn,
                            "default_data": [
                                {
                                    "key": "deck_name",
                                    "value": default_value
                                }
                            ]
                        }]
                    elif bin_type == "start_time":
                        if seat.game.start_time:
                            start_time = seat.game.start_time.strftime('%H')
                            default_value = f"{start_time}:00"
                        else:
                            start_time = "none"
                            default_value = "start time not recorded"
                        game_bins = [{
                            "bin_name": start_time,
                            "default_data": [
                                {
                                    "key": "deck_name",
                                    "value": default_value
                                }
                            ]
                        }]
                    elif bin_type == "end_time":
                        if seat.game.end_time:
                            end_time = seat.game.end_time.strftime('%H')
                            default_value = f"{end_time}:00"
                        else:
                            end_time = "none"
                            default_value = "end time not recorded"
                        game_bins = [{
                            "bin_name": end_time,
                            "default_data": [
                                {
                                    "key": "deck_name",
                                    "value": default_value
                                }
                            ]
                        }]
                    elif bin_type == "dow":
                        dow = seat.game.start_time.strftime('%A')
                        game_bins = [{
                            "bin_name": dow,
                            "default_data": [
                                {
                                    "key": "deck_name",
                                    "value": dow
                                }
                            ]
                        }]
                    elif bin_type == "month":
                        month = seat.game.start_time.strftime('%B')
                        game_bins = [{
                            "bin_name": month,
                            "default_data": [
                                {
                                    "key": "deck_name",
                                    "value": month
                                }
                            ]
                        }]
                    elif bin_type == "year":
                        year = seat.game.start_time.strftime('%Y')
                        game_bins = [{
                            "bin_name": year,
                            "default_data": [
                                {
                                    "key": "deck_name",
                                    "value": year
                                }
                            ]
                        }]
                    elif bin_type == "borrowed":
                        pilot = seat.player.player_name
                        if pilot == deck.player.player_name:
                            game_bins = [{
                                "bin_name": "owner",
                                "default_data": [
                                    {
                                        "key": "deck_name",
                                        "value": f"{pilot} (owner)"
                                    }
                                ]
                            }]
                        elif pilot != deck.player.player_name:
                            game_bins = [{
                                "bin_name": pilot,
                                "default_data": [
                                    {
                                        "key": "deck_name",
                                        "value": pilot
                                    }
                                ]
                            }]
                        else:
                            raise ValueError("somehow the pilot is neither the deck owner nor not the deck owner")
                    else:
                        game_bins = []

                    if game_bins:
                        for game_bin in game_bins:
                            # create bin if it doesn't exist yet
                            if game_bin["bin_name"] not in table_data[deck.id]:
                                table_data[deck.id][game_bin["bin_name"]] = defaultdict(int)
                                for default_datum in game_bin["default_data"]:
                                    table_data[deck.id][game_bin["bin_name"]][default_datum["key"]] = default_datum["value"]
                            # start populating the bins
                            table_data[deck.id][game_bin["bin_name"]]["num_games_played"] += 1

                    _, winning_deck = derived_quantities.game_winning_player_and_deck(seat.game)
                    if winning_deck.id == deck.id:
                        table_data[deck.id]["total"]["num_games_won"] += 1
                        if game_bins:
                            for game_bin in game_bins:
                                table_data[deck.id][game_bin["bin_name"]]["num_games_won"] += 1

                    _, game_seconds = derived_quantities.game_length_in_time(seat.game)
                    if game_seconds:
                        table_data[deck.id]["total"]["total_game_time"] += game_seconds
                        if game_bins:
                            for game_bin in game_bins:
                                table_data[deck.id][game_bin["bin_name"]]["total_game_time"] += game_seconds
                    game_length = derived_quantities.game_length_in_turns(seat.game)
                    if game_length:
                        table_data[deck.id]["total"]["total_game_turns"] += game_length
                        if game_bins:
                            for game_bin in game_bins:
                                table_data[deck.id][game_bin["bin_name"]]["total_game_turns"] += game_length
                    first_ko = derived_quantities.game_first_ko(seat.game)
                    if first_ko:
                        table_data[deck.id]["total"]["total_first_ko"] += first_ko
                        if game_bins:
                            for game_bin in game_bins:
                                table_data[deck.id][game_bin["bin_name"]]["total_first_ko"] += first_ko
                    most_recent_game["total"] = max(most_recent_game["total"], seat.game.start_time)
                    if game_bins:
                        for game_bin in game_bins:
                            if game_bin["bin_name"] in most_recent_game.keys():
                                most_recent_game[game_bin["bin_name"]] = max(most_recent_game[game_bin["bin_name"]], seat.game.start_time)
                            else:
                                most_recent_game[game_bin["bin_name"]] = seat.game.start_time

                for deck_bin in table_data[deck.id]:
                    # inititalise some values
                    if "num_games_won" not in table_data[deck.id][deck_bin]:
                        table_data[deck.id][deck_bin]["num_games_won"] = 0
                    # calculate some values
                    try:
                        table_data[deck.id][deck_bin]["win_rate"] = table_data[deck.id][deck_bin]["num_games_won"] / table_data[deck.id][deck_bin]["num_games_played"] * 100
                    except ZeroDivisionError:
                        table_data[deck.id][deck_bin]["win_rate"] = 0
                    try:
                        table_data[deck.id][deck_bin]["last_played"] = f"{(datetime.now() - most_recent_game[deck_bin]).days} days ago"
                    except KeyError:
                        table_data[deck.id][deck_bin]["last_played"] = "never"
                    if table_data[deck.id][deck_bin]["total_game_time"]:
                        try:
                            ave_time = table_data[deck.id][deck_bin]["total_game_time"] / table_data[deck.id][deck_bin]["num_games_played"]
                            table_data[deck.id][deck_bin]["ave_game_time"] = str(timedelta(seconds=(ave_time - (ave_time % 60))))[0:-3]
                        except ZeroDivisionError:
                            table_data[deck.id][deck_bin]["ave_game_time"] = ""
                    else:
                        table_data[deck.id][deck_bin]["ave_game_time"] = ""
                    if table_data[deck.id][deck_bin]['total_game_turns']:
                        try:
                            table_data[deck.id][deck_bin]["ave_game_turns"] = f"{(table_data[deck.id][deck_bin]['total_game_turns'] / table_data[deck.id][deck_bin]['num_games_played']):.1f}"
                        except ZeroDivisionError:
                            table_data[deck.id][deck_bin]["ave_game_turns"] = ""
                    else:
                        table_data[deck.id][deck_bin]["ave_game_turns"] = ""
                    if table_data[deck.id][deck_bin]['total_first_ko']:
                        try:
                            table_data[deck.id][deck_bin]["ave_first_ko"] = f"{(table_data[deck.id][deck_bin]['total_first_ko'] / table_data[deck.id][deck_bin]['num_games_played']):.1f}"
                        except ZeroDivisionError:
                            table_data[deck.id][deck_bin]["ave_first_ko"] = ""
                    else:
                        table_data[deck.id][deck_bin]["ave_first_ko"] = ""

        return render_template('data.html', data_type="deck", menu_data=html_data, table_data=table_data)
    elif request.form["type"] == "game":
        # Load the data we need
        games = game_crud.all(True)
        num_seats = 0
        games_to_remove = []

        for game in games:
            game.game_time, game.seconds = derived_quantities.game_length_in_time(game)
            game.game_turns = derived_quantities.game_length_in_turns(game)
            game.first_ko = derived_quantities.game_first_ko(game)
            seats = game_crud.get_child_data(game.id, "seat", True)
            game.player = [None] * len(seats)
            game.deck = [None] * len(seats)

            if request.form["requested_deck"] or request.form["player_name"]:
                deck_found = False
                player_found = False

                if request.form["requested_deck"]:
                    deck_name, _, query_tree = utils.get_deck_data_from_form_inputs(request.form['requested_deck'])
                    try:
                        requested_deck = deck_crud.specific(query_tree=query_tree,
                                                            join_classes=["player"],
                                                            return_model_object=True)[0]
                    except:
                        return errors.entry_not_found('data.html', [['deck', 'deck_name', deck_name]])

                for seat in seats:
                    if not request.form["requested_deck"] or seat.deck == requested_deck:
                        deck_found = True
                    if not request.form["player_name"] or seat.player.player_name == request.form["player_name"]:
                        player_found = True

                if not deck_found or not player_found:
                    games_to_remove.append(game)

            winning_player, winning_deck = derived_quantities.game_winning_player_and_deck(game)
            winning_player = player_crud.specific(key="id", value=winning_player.id, return_model_object=True)[0]
            winning_deck = deck_crud.specific(key="id", value=winning_deck.id, return_model_object=True)[0]

            game.winner = winning_player.player_name + " - " + winning_deck.deck_name
            if winning_player.player_name != winning_deck.player.player_name:
                game.winner += f" ({winning_deck.player.player_name}'s deck)"

            for seat in seats:
                game.player[seat.seat_no - 1] = seat.player
                game.deck[seat.seat_no - 1] = seat.deck

            if len(seats) > num_seats and game not in games_to_remove:
                num_seats = len(seats)

        for game_to_remove in games_to_remove:
            games.remove(game_to_remove)

        # Prepare data to pass to the template
        html_data = {"colour_identities": colour_identities,
                     "decks": decks,
                     "games": games,
                     "players": players,
                     "num_seats": num_seats}

        return render_template('data.html', data_type="game", menu_data=html_data)
    elif request.form["type"] == "player":
        # generate the full list of edhrec deck data
        min_edhrec_decks = min([deck.edhrec_num_decks for deck in decks if isinstance(deck.edhrec_num_decks, int)])
        page = 1
        edhrec_all_cmdrs_response = requests.get("https://json.edhrec.com/pages/commanders/year.json").json()
        popularity_list = edhrec_all_cmdrs_response["container"]["json_dict"]["cardlists"][0]["cardviews"]
        while popularity_list[-1]["num_decks"] > min_edhrec_decks:
            edhrec_all_cmdrs_response = requests.get(f"https://json.edhrec.com/pages/commanders/year-past2years-{page}.json").json()
            popularity_list += edhrec_all_cmdrs_response["cardviews"]
            page += 1

        # find restrictions
        restrictions = []
        for form_item in request.form:
            if form_item != "type" and form_item != "bins" and request.form[form_item]:
                restriction_key = form_item
                restriction_value = request.form[form_item]

                # this wants to be a select case, but I'm using Python 3.8 :(
                if form_item == "ci_abbr":
                    # check that colour identity exists in database, return an error if it doesn't
                    colour_identity_data, desired_ci = utils.get_ci_data_from_list_of_colours(request.form.getlist("ci_abbr"))
                    if not colour_identity_data:
                        return errors.entry_not_found('data.html', [["colour_identity", "colours", desired_ci]])
                    restriction_key = "ci_name"
                    restriction_value = colour_identity_data[0].ci_name

                    class_type = "colour_identity"

                else:
                    return errors.missing_form_item('data.html')

                restrictions.append({
                    "class_type": class_type,
                    "key": restriction_key,
                    "value": restriction_value
                })

        # set up our initial bins
        if "bins" in request.form.keys():
            bin_type = request.form["bins"]
        else:
            bin_type = ""

        table_data = {}

        for player in players:
            # initialise data
            table_data[player.id] = {"total": defaultdict(int)}
            table_data[player.id]["total"]["player_name"] = player.player_name

            # loop over all of that player's decks
            for deck in player.decks:
                # skip this deck if it doesn't meet the restrictions
                if restrictions:
                    skip = False
                    for restriction in restrictions:
                        parent_data = deck_crud.get_parent_data(deck.id, restriction["class_type"], True)
                        if getattr(parent_data[0], restriction["key"]) != restriction["value"]:
                            skip = True

                    if skip:
                        continue

                # increment the number of decks counter
                table_data[player.id]["total"]["num_decks"] += 1

                # find the EDHrec data for this deck
                if (not deck.last_accessed
                    or ((datetime.now() - datetime.strptime(str(deck.last_accessed), "%Y-%m-%d %H:%M:%S"))
                        > timedelta(hours=5, minutes=59))
                ):
                    try:
                        edhrec_uri = curl_utils.get_edhrec_uri_from_commander_names([deck.commander_name,
                                                                                     deck.partner_name])
                        edhrec_decks, popularity = curl_utils.get_popularity_from_edhrec_uri(edhrec_uri)
                        table_data[player.id]["total"]["edhrec_decks"] += edhrec_decks
                        deck_crud.update(deck.id, jsonify({"edhrec_num_decks": edhrec_decks,
                                                            "edhrec_popularity": popularity,
                                                            "last_accessed": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}))
                        time.sleep(0.01)
                    except:
                        pass
                else:
                    table_data[player.id]["total"]["edhrec_decks"] += deck.edhrec_num_decks

            # if we have no decks that match the restrictions, we can skip this player
            if table_data[player.id]["total"]["num_decks"] == 0:
                table_data.pop(player.id)
                continue

            # find the ranking that the player's average deck would have on EDHrec
            rank = 0
            table_data[player.id]["total"]["ave_edhrec_decks"] = table_data[player.id]["total"]["edhrec_decks"] / table_data[player.id]["total"]["num_decks"]
            while table_data[player.id]["total"]["ave_edhrec_decks"] < popularity_list[rank]["num_decks"]:
                rank += 1
            table_data[player.id]["total"]["ave_edhrec_ranking"] = f"#{rank + 1} ({popularity_list[rank]['name']})"

            # find all the games this player has played
            player_seats = player_crud.get_child_data(player.id, "seat", True)

            for seat in player_seats:
                # skip this game if the played deck doesn't meet the restrictions
                if restrictions:
                    skip = False
                    for restriction in restrictions:
                        parent_data = deck_crud.get_parent_data(seat.deck.id, restriction["class_type"], True)
                        if getattr(parent_data[0], restriction["key"]) != restriction["value"]:
                            skip = True

                    if skip:
                        continue

                table_data[player.id]["total"]["num_games_played"] += 1

                # find the type of bins we want, if any, and set the specific bins we want for this game
                # this wants to be a select case, but I'm using Python 3.8 :(
                if bin_type == "opp_player":
                    game_bins = []
                    opponents = seat.game.seats
                    for opponent in opponents:
                        if opponent.id != seat.id:
                            game_bins.append({
                                "bin_name": opponent.player_id,
                                "default_data": [
                                    {
                                        "key": "player_name",
                                        "value": f"vs {opponent.player.player_name}"
                                    }
                                ]
                            })
                elif bin_type == "opp_deck":
                    game_bins = []
                    opponents = seat.game.seats
                    for opponent in opponents:
                        if opponent.id != seat.id:
                            game_bins.append({
                                "bin_name": opponent.deck_id,
                                "default_data": [
                                    {
                                        "key": "player_name",
                                        "value": f"vs {opponent.deck.deck_name}"
                                    },
                                    {
                                        "key": "num_decks",
                                        "value": f"{opponent.deck.player.player_name}'s deck"
                                    }
                                ]
                            })
                elif bin_type == "opp_ci":
                    game_bins = []
                    opponents = seat.game.seats
                    opp_ci    = []
                    for opponent in opponents:
                        if opponent.id != seat.id:
                            if opponent.deck.colour_identity.ci_name not in opp_ci:
                                game_bins.append({
                                    "bin_name": opponent.deck.colour_identity.ci_name,
                                    "default_data": [
                                        {
                                            "key": "player_name",
                                            "value": f"vs {opponent.deck.colour_identity.ci_name}"
                                        },
                                        {
                                            "key": "colours",
                                            "value": f"{opponent.deck.colour_identity.colours}"
                                        }
                                    ]
                                })
                                opp_ci.append(opponent.deck.colour_identity.ci_name)
                elif bin_type == "opp_num_colours":
                    game_bins       = []
                    opponents       = seat.game.seats
                    opp_num_colours = []
                    for opponent in opponents:
                        if opponent.id != seat.id:
                            if len(opponent.deck.colour_identity.colours) not in opp_num_colours:
                                game_bins.append({
                                    "bin_name": len(opponent.deck.colour_identity.colours),
                                    "default_data": [
                                        {
                                            "key": "player_name",
                                            "value": f"vs {len(opponent.deck.colour_identity.colours)} colour decks"
                                        }
                                    ]
                                })
                                opp_num_colours.append(len(opponent.deck.colour_identity.colours))
                elif bin_type == "num_players":
                    num_players = len(seat.game.seats)
                    game_bins = [{
                        "bin_name": num_players,
                        "default_data": [
                            {
                                "key": "player_name",
                                "value": f"{num_players} player games"
                            }
                        ]
                    }]
                elif bin_type == "seat":
                    game_bins = [{
                        "bin_name": seat.seat_no,
                        "default_data": [
                            {
                                "key": "player_name",
                                "value": f"seat number {seat.seat_no}"
                            }
                        ]
                    }]
                elif bin_type == "result":
                    winning_player, _ = derived_quantities.game_winning_player_and_deck(seat.game)
                    if winning_player.id == player.id:
                        game_bins = [{
                            "bin_name": "win",
                            "default_data": [
                                {
                                    "key": "player_name",
                                    "value": "Games Won"
                                }
                            ]
                        }]
                    else:
                        game_bins = [{
                            "bin_name": "loss",
                            "default_data": [
                                {
                                    "key": "player_name",
                                    "value": "Games Lost"
                                }
                            ]
                        }]
                elif bin_type == "game_time":
                    _, game_time = derived_quantities.game_length_in_time(seat.game)
                    if game_time:
                        game_minutes = game_time / 60
                        minutes_bin = int(game_minutes - (game_minutes % 10))
                        default_value = f"{minutes_bin} - {minutes_bin + 10} minute games"
                    else:
                        minutes_bin = "untimed"
                        default_value = "untimed games"
                    game_bins = [{
                        "bin_name": minutes_bin,
                        "default_data": [
                            {
                                "key": "player_name",
                                "value": default_value
                            }
                        ]
                    }]
                elif bin_type == "game_turns":
                    game_length = derived_quantities.game_length_in_turns(seat.game)
                    game_bins = [{
                        "bin_name": game_length,
                        "default_data": [
                            {
                                "key": "player_name",
                                "value": f"{game_length} turn games"
                            }
                        ]
                    }]
                elif bin_type == "first_KO":
                    KO_turn = derived_quantities.game_first_ko(seat.game)
                    game_bins = [{
                        "bin_name": KO_turn,
                        "default_data": [
                            {
                                "key": "player_name",
                                "value": f"turn {KO_turn} KO"
                            }
                        ]
                    }]
                elif bin_type == "self_KO":
                    KO_turn = seat.ko_turn
                    if KO_turn:
                        default_value = f"KO'd on turn {KO_turn}"
                    else:
                        KO_turn = "win"
                        default_value = "Won the game"
                    game_bins = [{
                        "bin_name": KO_turn,
                        "default_data": [
                            {
                                "key": "player_name",
                                "value": default_value
                            }
                        ]
                    }]
                elif bin_type == "start_time":
                    if seat.game.start_time:
                        start_time = seat.game.start_time.strftime('%H')
                        default_value = f"{start_time}:00"
                    else:
                        start_time = "none"
                        default_value = "start time not recorded"
                    game_bins = [{
                        "bin_name": start_time,
                        "default_data": [
                            {
                                "key": "player_name",
                                "value": default_value
                            }
                        ]
                    }]
                elif bin_type == "end_time":
                    if seat.game.end_time:
                        end_time = seat.game.end_time.strftime('%H')
                        default_value = f"{end_time}:00"
                    else:
                        end_time = "none"
                        default_value = "end time not recorded"
                    game_bins = [{
                        "bin_name": end_time,
                        "default_data": [
                            {
                                "key": "player_name",
                                "value": default_value
                            }
                        ]
                    }]
                elif bin_type == "dow":
                    dow = seat.game.start_time.strftime('%A')
                    game_bins = [{
                        "bin_name": dow,
                        "default_data": [
                            {
                                "key": "player_name",
                                "value": dow
                            }
                        ]
                    }]
                elif bin_type == "month":
                    month = seat.game.start_time.strftime('%B')
                    game_bins = [{
                        "bin_name": month,
                        "default_data": [
                            {
                                "key": "player_name",
                                "value": month
                            }
                        ]
                    }]
                elif bin_type == "year":
                    year = seat.game.start_time.strftime('%Y')
                    game_bins = [{
                        "bin_name": year,
                        "default_data": [
                            {
                                "key": "player_name",
                                "value": year
                            }
                        ]
                    }]
                elif bin_type == "borrowed":
                    owner = seat.deck.player
                    if owner.player_name == player.player_name:
                        game_bins = [{
                            "bin_name": "owner",
                            "default_data": [
                                {
                                    "key": "player_name",
                                    "value": f"Playing {owner.player_name}'s deck"
                                }
                            ]
                        }]
                    elif owner.player_name != player.player_name:
                        game_bins = [{
                            "bin_name": owner.player_name,
                            "default_data": [
                                {
                                    "key": "player_name",
                                    "value": f"Playing {owner.player_name}'s deck"
                                }
                            ]
                        }]
                    else:
                        raise ValueError("somehow the pilot is neither the deck owner nor not the deck owner")
                else:
                    game_bins = []

                if game_bins:
                    for game_bin in game_bins:
                        # create bin if it doesn't exist yet
                        if game_bin["bin_name"] not in table_data[player.id]:
                            table_data[player.id][game_bin["bin_name"]] = defaultdict(int)
                            for default_datum in game_bin["default_data"]:
                                table_data[player.id][game_bin["bin_name"]][default_datum["key"]] = default_datum["value"]
                        # start populating the bins
                        table_data[player.id][game_bin["bin_name"]]["num_games_played"] += 1

                winning_player, _ = derived_quantities.game_winning_player_and_deck(seat.game)
                if winning_player.id == player.id:
                    table_data[player.id]["total"]["num_games_won"] += 1
                    if game_bins:
                        for game_bin in game_bins:
                            table_data[player.id][game_bin["bin_name"]]["num_games_won"] += 1

                _, game_seconds = derived_quantities.game_length_in_time(seat.game)
                if game_seconds:
                    table_data[player.id]["total"]["total_game_time"] += game_seconds
                    if game_bins:
                        for game_bin in game_bins:
                            table_data[player.id][game_bin["bin_name"]]["total_game_time"] += game_seconds
                game_length = derived_quantities.game_length_in_turns(seat.game)
                if game_length:
                    table_data[player.id]["total"]["total_game_turns"] += game_length
                    if game_bins:
                        for game_bin in game_bins:
                            table_data[player.id][game_bin["bin_name"]]["total_game_turns"] += game_length
                first_ko = derived_quantities.game_first_ko(seat.game)
                if first_ko:
                    table_data[player.id]["total"]["total_first_ko"] += first_ko
                    if game_bins:
                        for game_bin in game_bins:
                            table_data[player.id][game_bin["bin_name"]]["total_first_ko"] += first_ko

            for player_bin in table_data[player.id]:
                # inititalise some values
                if "num_games_won" not in table_data[player.id][player_bin]:
                    table_data[player.id][player_bin]["num_games_won"] = 0
                # calculate some values
                try:
                    table_data[player.id][player_bin]["win_rate"] = table_data[player.id][player_bin]["num_games_won"] / table_data[player.id][player_bin]["num_games_played"] * 100
                except ZeroDivisionError:
                    table_data[player.id][player_bin]["win_rate"] = 0
                if table_data[player.id][player_bin]["total_game_time"]:
                    try:
                        ave_time = table_data[player.id][player_bin]["total_game_time"] / table_data[player.id][player_bin]["num_games_played"]
                        table_data[player.id][player_bin]["ave_game_time"] = str(timedelta(seconds=(ave_time - (ave_time % 60))))[0:-3]
                    except ZeroDivisionError:
                        table_data[player.id][player_bin]["ave_game_time"] = ""
                else:
                    table_data[player.id][player_bin]["ave_game_time"] = ""
                if table_data[player.id][player_bin]['total_game_turns']:
                    try:
                        table_data[player.id][player_bin]["ave_game_turns"] = f"{(table_data[player.id][player_bin]['total_game_turns'] / table_data[player.id][player_bin]['num_games_played']):.1f}"
                    except ZeroDivisionError:
                        table_data[player.id][player_bin]["ave_game_turns"] = ""
                else:
                    table_data[player.id][player_bin]["ave_game_turns"] = ""
                if table_data[player.id][player_bin]['total_first_ko']:
                    try:
                        table_data[player.id][player_bin]["ave_first_ko"] = f"{(table_data[player.id][player_bin]['total_first_ko'] / table_data[player.id][player_bin]['num_games_played']):.1f}"
                    except ZeroDivisionError:
                        table_data[player.id][player_bin]["ave_first_ko"] = ""
                else:
                    table_data[player.id][player_bin]["ave_first_ko"] = ""

        return render_template('data.html', data_type="player", menu_data=html_data, table_data=table_data)

    # Prepare data to pass to the template
    html_data = {"colour_identities": colour_identities,
                 "decks": decks,
                 "players": players}

    return render_template('data.html', menu_data=html_data)

@app.route('/graphs', methods=['GET', 'POST'])
def graphs():
    """ Graphs are displayed here """
    # Load the data we need before passing it to the template
    html_data = {"decks": deck_crud.all(True),
                 "players": player_crud.all(True)}
    if request.method == 'GET':
        deck_data = deck_crud.all(True)

        plt_data = {}

        for ii in list(range(0,6)):
            plt_data.update({f"{ii} colours": 0})

        for deck in deck_data:
            deck_num_colours = deck.colour_identity.num_colours
            plt_data[f"{deck_num_colours} colours"] += 1

        number_of_colours = list(plt_data.keys())
        number_of_decks = list(plt_data.values())

        example_bar_chart = bar_charts.make_bar_chart(number_of_colours,
                                                      number_of_decks,
                                                      "Number of Colours",
                                                      "Number of Decks",
                                                      "Number of Decks per Number of Colours")
        example_pie_chart = pie_charts.make_pie_chart(number_of_colours,
                                                      number_of_decks,
                                                      "Number of Decks per Number of Colours")

        return render_template(
            'graphs.html',
            data=html_data,
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
            },
            "player": {
                "file": "player",
                "class": "player_crud",
                "name_column": "player_name"
            }
        }
        titles = {
            "colour": "Colour",
            "colour identity": "Colour Identity",
            "deck": "Number of Decks",
            "number of colours": "Number of Colours",
            "number of decks": "Number of Decks",
            "owner": "player",
            "win rate": "Win Rate"
        }

        if request.form['type'] == "bar":
            if request.form["bar_data"] not in list(model_names.keys()):
                call_error = True
                missing_entries.append([request.form["bar_data"], 'Data Type'])
                return errors.option_not_available('graphs.html', missing_entries)

            no_zeroes = bool("no_zeroes" in request.form)

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
                        datum_colours = datum.colour_identity.colours
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
                colour_identities = colour_identity_crud.all(True)

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
                    xy_data.update({f"{ii} colours": 0})

                if request.form["bar_y"] == "number of decks":
                    for datum in data:
                        datum_num_colours = datum.colour_identity.num_colours
                        xy_data[f"{datum_num_colours} colours"] += 1
                else:
                    call_error = True
                    missing_entries.append([request.form["bar_y"], 'Y axis'])
            elif request.form["bar_x"] == "owner":
                players = player_crud.all(True)

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
                        games_played = deck_crud.get_child_data(getattr(datum, "id"), "seat", True)
                        num_games_played = len(games_played)

                        if num_games_played == 0:
                            xy_data[datum_owner] = 0
                        else:
                            num_games_won = 0
                            for seat in games_played:
                                _, winning_deck = derived_quantities.game_winning_player_and_deck(seat.game)
                                if winning_deck.id == deck.id:
                                    num_games_won += 1
                            xy_data[datum_owner] = num_games_won / num_games_played * 100
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
                            games_played = deck_crud.get_child_data(getattr(datum, "id"), "seat", True)
                            num_games_played = len(games_played)

                            if num_games_played == 0:
                                xy_data[datum_name] = 0
                            else:
                                num_games_won = 0
                                for seat in games_played:
                                    _, winning_deck = derived_quantities.game_winning_player_and_deck(seat.game)
                                    if winning_deck.id == deck.id:
                                        num_games_won += 1
                                xy_data[datum_name] = num_games_won / num_games_played * 100
            else:
                call_error = True
                missing_entries.append([request.form["bar_x"], 'X axis'])

            if call_error:
                return errors.option_not_available('graphs.html', missing_entries)

            x_values = list(xy_data.keys())
            y_values = list(xy_data.values())

            plt_graph = bar_charts.make_bar_chart(x_values,
                                                  y_values,
                                                  titles[request.form["bar_x"]],
                                                  titles[request.form["bar_y"]],
                                                  titles[request.form["bar_y"]] + " per " + titles[request.form["bar_x"]],
                                                  no_zeroes)
        elif request.form['type'] == "line":
            if request.form["line_data"] not in list(model_names.keys()):
                call_error = True
                missing_entries.append([request.form["line_data"], 'Data Type'])
                return errors.option_not_available('graphs.html', missing_entries)

            crud_file = importlib.import_module("crud." + model_names[request.form["line_data"]]["file"])
            crud_class = getattr(crud_file, model_names[request.form["line_data"]]["class"])

            if request.form["line_data"] == "deck":
                data = []
                data_names = request.form.getlist("line_" + request.form['line_data'])
                for deck_input in data_names:
                    if deck_input:
                        deck_name, _, query_tree = utils.get_deck_data_from_form_inputs(deck_input)
                        try:
                            data.append(crud_class.specific(query_tree=query_tree,
                                                            join_classes=["player"],
                                                            return_model_object = True)[0])
                        except:
                            return errors.entry_not_found('data.html', [['deck', 'deck_name', deck_name]])
            else:
                data = []
                data_names = request.form.getlist("line_" + request.form['line_data'])
                for datum_name in data_names:
                    if datum_name:
                        data.append(crud_class.specific(key=request.form['line_data'] + "_name",
                                                        value=datum_name,
                                                        return_model_object = True)[0])

            # this wants to be a select case, but I'm using Python 3.8 :(
            if request.form["line_x"] == "time":
                if request.form["line_y"] == "win rate":
                    time_axis = []
                    win_rates = []
                    for datum in data:
                        if not datum:
                            continue

                        seats = datum.seats
                        games = []
                        time_data = []
                        for seat in seats:
                            games.append(seat.game)

                            game_year = int(str(seat.game.start_time)[:4])
                            game_month = int(str(seat.game.start_time)[5:7])
                            game_day = int(str(seat.game.start_time)[8:10])
                            time_data.append(datetime(game_year, game_month, game_day) + timedelta(days=1))

                            time_data.append(datetime.now())
                            time_data = list(set(time_data))    # set removes duplicated values
                            time_data.sort()

                            win_rate_over_time = [0] * len(time_data)
                            games_played_over_time = [0] * len(time_data)
                            games_won_over_time = [0] * len(time_data)
                            for i in range(len(time_data)):
                                for game in games:
                                    if game.start_time < time_data[i]:
                                        games_played_over_time[i] += 1
                                        winning_player, winning_deck = derived_quantities.game_winning_player_and_deck(game)
                                        if winning_player.id == datum.id or winning_deck.id == datum.id:
                                            games_won_over_time[i] += 1
                                if games_played_over_time[i] == 0:
                                    win_rate_over_time[i] = 0
                                else:
                                    win_rate_over_time[i] = games_won_over_time[i] / games_played_over_time[i] * 100

                        time_axis.append(time_data)
                        win_rates.append(win_rate_over_time)

                    plt_graph = line_graphs.make_line_graph(x_values = time_axis,
                                                            y_values = win_rates,
                                                            x_label = "Time",
                                                            y_label = "Win Rate",
                                                            title = "win rate over time",
                                                            legend = data_names)
                else:
                    call_error = True
                    missing_entries.append([request.form["line_y"], 'Y Axis'])
            else:
                call_error = True
                missing_entries.append([request.form["line_x"], 'X Axis'])

            if call_error:
                return errors.option_not_available('graphs.html', missing_entries)
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
                colour_identities = colour_identity_crud.all(True)

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
                    pie_data.update({f"{ii} colours": 0})

                for datum in data:
                    datum_num_colours = datum.colour_identity.num_colours
                    pie_data[f"{datum_num_colours} colours"] += 1
            elif request.form["pie_divisions"] == "owner":
                players = player_crud.all(True)

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

            plt_graph = pie_charts.make_pie_chart(labels,
                                                  values,
                                                  titles[request.form["pie_data"]] + " per " + titles[request.form["pie_divisions"]])
        else:
            return errors.missing_form_item('graphs.html')

        return render_template(
            'graphs.html',
            data=html_data,
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
def error_404(_):
    return render_template('404.html')

# Set debug=True for the server to auto-reload when there are changes
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

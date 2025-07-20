''' utils that involve curl commands '''
import requests
from errors import errors

def get_commander_name_from_commander_id(commander_id):
    response = requests.get(f"https://api.scryfall.com/cards/{commander_id}").json()
    if "status" in response:
        raise ValueError("unable to get data from scryfall")

    return response["name"], response["related_uris"]["edhrec"]

def get_popularity_from_commander_id(commander_id):
    scryfall_response = requests.get(f"https://api.scryfall.com/cards/{commander_id}").json()
    if "status" in scryfall_response:
        return errors.card_not_found('input.html', [scryfall_response["details"]], 'create')

    commander_name = scryfall_response["scryfall_uri"].split('/')[-1].split('?')[0]

    try:
        edhrec_response = requests.get(f"https://json.edhrec.com/pages/commanders/{commander_name}.json").json()
    except:
        raise ValueError("unable to get data from edhrec")
    label = edhrec_response["container"]["json_dict"]["card"]["label"].split()
    return label[0], label[-1]

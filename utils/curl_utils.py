''' utils that involve curl commands '''
import requests
from errors import errors

def get_edhrec_uri_from_commander_names(cmdr_names=[]):
    names = ""
    for cmdr_name in cmdr_names:
        cmdr = cmdr_name.split('/')[0]
        cmdr = cmdr.replace(',','')
        cmdr = cmdr.replace("'",'')
        cmdr = cmdr.replace(' ','-')
        if cmdr[-1] == "-":
            names += cmdr.lower()
        else:
            names += cmdr.lower() + "-"

    return f"/commanders/{names[:-1]}"

def get_commander_name_from_commander_id(commander_id):
    response = requests.get(f"https://api.scryfall.com/cards/{commander_id}").json()
    if "status" in response:
        raise ValueError("unable to get data from scryfall")

    return response["name"], get_edhrec_uri_from_commander_names([response["name"]])

def get_popularity_from_edhrec_uri(edhrec_uri):
    uri = f"https://json.edhrec.com/pages{edhrec_uri}.json"
    try:
        edhrec_response = requests.get(uri).json()
    except:
        raise ValueError("unable to get data from edhrec")
    if "redirect" in edhrec_response:
        uri = f"https://json.edhrec.com/pages{edhrec_response['redirect']}.json"
        try:
            edhrec_response = requests.get(uri).json()
        except:
            raise ValueError("unable to get data from edhrec")
    label = edhrec_response["container"]["json_dict"]["card"]["label"].split()
    return label[0], label[-1]

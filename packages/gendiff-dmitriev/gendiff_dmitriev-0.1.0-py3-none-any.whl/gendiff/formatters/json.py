import json


def make_json(data):
    """Shows the complete difference between files as a json file"""
    return json.dumps(data, indent=2)

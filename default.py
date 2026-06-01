import json

data = {"msg": "No Wild Animals", "anm": []}

with open('static/data.json', 'w') as file:
            json.dump(data, file)
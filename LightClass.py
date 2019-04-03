import requests


class Light:
    def __init__(self, light_id, name, state, color):
        self.variables = {
            'id': light_id,
            'name': name,
            'state': state,
            'color': color,
            'selected': False
        }

    def get(self, variable):
        return self.variables[variable]

    def set(self, variable, value):
        self.variables[variable] = value

    def toggle(self, ipBridge, username):
        if not self.get('selected'):
            return
        if self.get('state'):
            response = requests.put('http://' + ipBridge + "/api/" + username + "/lights/" + self.get('id') + "/state",
                                "{\"on\": false}")
        else:
            response = requests.put('http://' + ipBridge + "/api/" + username + "/lights/" + self.get('id') + "/state",
                                "{\"on\": true}")

        self.set('state', not self.get('state'))

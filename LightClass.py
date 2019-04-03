import requests


class Light:
    def __init__(self, light_id, name, state, color, ipBridge, username):
        self.variables = {
            'id': light_id,
            'name': name,
            'state': state,
            'color': color,
            'selected': False,
            'link': 'http://' + ipBridge + "/api/" + username + "/lights/" + light_id
        }

    def get(self, variable):
        return self.variables[variable]

    def set(self, variable, value):
        self.variables[variable] = value

    def toggle(self):
        if not self.get('selected'):
            return
        if self.get('state'):
            requests.put(self.get('link') + "/state", "{\"on\": false}")
        else:
            requests.put(self.get('link') + "/state", "{\"on\": true}")

        self.set('state', not self.get('state'))

    def color(self):
        if not self.get('selected'):
            return

        requests.put(self.get('link') + "/state", "{\"on\": true, \"xy\": \"" + str(self.get('color')) + "\"}")

    def colorloop(self):
        if not self.get('selected'):
            return

        requests.put(self.get('link') + "/state", "{\"on\": true, \"effect\": \"colorloop\"}")

    def alert(self):
        if not self.get('selected'):
            return

        requests.put(self.get('link') + "/state", "{\"on\": true, \"alert\": \"lselect\"}")

import requests


class Light:
    def __init__(self, light_id, name, state, color, ipBridge, username):
        self.variables = {
            'id': light_id,
            'name': name,
            'state': state,
            'color': list(color),
            'selected': False,
            'link': 'http://' + ipBridge + "/api/" + username + "/lights/" + light_id,
            'widget': None,
        }

    def get(self, variable):
        return self.variables[variable]

    def set(self, variable, value):
        self.variables[variable] = value

    def toggle(self, hex_color):
        if not self.get('selected'):
            return
        if self.get('state'):
            requests.put(self.get('link') + "/state", "{\"on\": false}")
        else:
            requests.put(self.get('link') + "/state", "{\"on\": true}")

        self.set('state', not self.get('state'))
        name, color = self.get('widget')
        if self.get('state'):
            color.config(bg=hex_color)
        else:
            color.config(bg='#000000')

    def color(self, xy, hex_color):
        if not self.get('selected'):
            return

        self.set('color', xy)
        requests.put(self.get('link') + "/state", "{\"on\": true, \"xy\": " + str(self.get('color')) + "}")

        self.set_widget_color(hex_color)

    def set_widget_color(self, hex_color):
        if not self.get('selected'):
            return

        name, color = self.get('widget')

        if self.get('state'):
            color.config(bg=hex_color)
        else:
            color.config(bg="#000000")

    def colorloop(self):
        if not self.get('selected'):
            return

        requests.put(self.get('link') + "/state", "{\"on\": true, \"effect\": \"colorloop\"}")

    def alert(self):
        if not self.get('selected'):
            return

        requests.put(self.get('link') + "/state", "{\"on\": true, \"alert\": \"lselect\"}")

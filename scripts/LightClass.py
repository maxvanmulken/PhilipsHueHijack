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

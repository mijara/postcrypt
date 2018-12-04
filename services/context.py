import pystache


class Context:
    def __init__(self):
        self.variables = {}
        self.headers = {}

    def has_var(self, key):
        return key in self.variables

    def get_var(self, key):
        return self.variables[key]

    def set_var(self, key, value):
        self.variables[key] = value

    def set_header(self, key, value):
        self.headers[key] = value

    def get_header(self, key):
        return self.headers[key]

    def render(self, value):
        return pystache.render(value, self.variables)

    def render_with_headers(self, value):
        context = {}

        context.update(self.variables)
        context.update(self.headers)

        return pystache.render(value, context)

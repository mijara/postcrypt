import statements


class Parser:
    def __init__(self, file_path):
        with open(file_path) as scrypt:
            self.text = scrypt.read()

    def next_token(self):
        token = ''

        for i, c in enumerate(self.text):
            if not c.isspace():
                token += c
            else:
                self.text = self.text[(i + 1):]

                return token.strip()

        # clear the last token in the file.
        if token:
            self.text = ''
            return token.strip()

        raise ValueError('incomplete file')

    def next_line(self):
        token = ''

        for i, c in enumerate(self.text):
            if c == '\n':
                self.text = self.text[(i + 1):]
                return token.strip()
            else:
                token += c

    def parse_json(self):
        complete_token = ''

        while True:
            token = self.next_line()

            if not token:
                return complete_token
            else:
                complete_token += token

    def parse_post(self):
        url = self.next_token()
        json_token = self.parse_json()

        return statements.PostStatement(url, json_token)

    def parse_put(self):
        url = self.next_token()
        data = self.parse_json()

        return statements.PutStatement(url, data)

    def parse_delete(self):
        url = self.next_token()

        return statements.DeleteStatement(url)

    def parse_get(self):
        url = self.next_token()
        return statements.GetStatement(url)

    def parse_var(self):
        name = self.next_token()
        assert self.next_token() == '='
        value = self.next_line()

        return statements.VariableStatement(name, value)

    def parse_header(self):
        key = self.next_token()
        assert self.next_token() == '='
        value = self.next_line()

        return statements.HeaderStatement(key, value)

    def parse_input(self):
        variable = self.next_token()

        return statements.InputStatement(variable)

    def parse_load(self):
        file_path = self.next_line()

        return statements.LoadStatement(file_path)

    def parse_log(self):
        tag = self.next_token()
        text = self.next_line()

        return statements.LogStatement(tag, text)

    def parse_mode(self):
        mode = self.next_token()

        return statements.ModeStatement(mode)

    def parse_statement(self):
        token = self.next_token()

        if token == 'post':
            return self.parse_post()
        elif token == 'put':
            return self.parse_put()
        elif token == 'delete':
            return self.parse_delete()
        elif token == 'get':
            return self.parse_get()
        elif token == 'input':
            return self.parse_input()
        elif token == 'load':
            return self.parse_load()
        elif token == 'var':
            return self.parse_var()
        elif token == 'header':
            return self.parse_header()
        elif token == 'log':
            return self.parse_log()
        elif token == 'mode':
            return self.parse_mode()
        elif token:
            raise Parser.ParseError(f'unexpected token {token}')

    def process(self):
        statements = []

        while self.text:
            statement = self.parse_statement()

            if statement:
                statements.append(statement)

        return statements

    class ParseError(Exception):
        pass

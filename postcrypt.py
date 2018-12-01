import json
import os

import pystache
import requests
from termcolor import colored

import statements
from parser import Parser


class Postcrypt:
    verbs = ['variable', 'request', 'header', 'get']

    def __init__(self, main_file, mode=None):
        self.main_file = main_file
        self.mode = 'none' if mode is None else mode

        self.base_path = os.path.dirname(main_file)

        self.just = max(len(v) for v in Postcrypt.verbs)

        # execution variables.
        self.statements = []
        self.context = {}
        self.headers = {}
        self.last_response = {}
        self.skip_mode = False

    def process(self):
        self.load_file(file_path=self.main_file)

        try:
            # main executor.
            while len(self.statements) != 0:
                statement = self.statements.pop(0)

                if self.skip_mode:
                    if isinstance(statement, statements.ModeStatement) and statement.mode == self.mode:
                        self.handle_statement(statement)
                        self.skip_mode = False
                else:
                    self.handle_statement(statement)

            # log the last response.
            if 'response' in self.context:
                self.log('response', self.main_file, '>>>')
                print(json.dumps(self.context['response'], indent=2))
        except requests.exceptions.ConnectionError as e:
            if e.response is not None:
                self.error(f'{e.response.status_code} {e.response.text}')
            else:
                self.error(f'{e.strerror}')

    def handle_statement(self, statement):
        if isinstance(statement, statements.LoadStatement):
            self.handle_load_statement(statement)
        elif isinstance(statement, statements.PostStatement):
            self.handle_post_statement(statement)
        elif isinstance(statement, statements.PutStatement):
            self.handle_put_statement(statement)
        elif isinstance(statement, statements.GetStatement):
            self.handle_get_statement(statement)
        elif isinstance(statement, statements.DeleteStatement):
            self.handle_delete_statement(statement)
        elif isinstance(statement, statements.VariableStatement):
            self.handle_variable_statement(statement)
        elif isinstance(statement, statements.HeaderStatement):
            self.handle_header_statement(statement)
        elif isinstance(statement, statements.LogStatement):
            self.handle_log_statement(statement)
        elif isinstance(statement, statements.InputStatement):
            self.handle_input_statement(statement)
        elif isinstance(statement, statements.ModeStatement):
            self.handle_mode_statement(statement)

    def handle_load_statement(self, load_statement):
        parser = Parser(os.path.join(self.base_path, load_statement.file_path))

        statements = parser.process()

        for i in range(len(statements) - 1, -1, -1):
            self.statements.insert(0, statements[i])

        self.log('LOAD', load_statement.file_path, f'{len(statements)} statement(s)')

    def _process_response(self, response):
        if response.ok:
            self.context['response'] = json.loads(response.text)
        else:
            raise requests.exceptions.ConnectionError(response=response)

    def handle_post_statement(self, statement):
        url = self.with_context(statement.url)
        body = self.with_context(statement.body)

        self.log('request', 'post', url)
        self._process_response(requests.post(url, json=json.loads(body), headers=self.headers))

    def handle_put_statement(self, statement):
        url = self.with_context(statement.url)
        body = self.with_context(statement.body)

        self.log('request', 'put', url)
        self._process_response(requests.put(url, json=json.loads(body), headers=self.headers))

    def handle_delete_statement(self, statement):
        url = self.with_context(statement.url)

        self.log('request', 'delete', url)
        self._process_response(requests.delete(url, headers=self.headers))

    def handle_get_statement(self, statement):
        url = self.with_context(statement.url)

        self.log('request', 'get', url)
        self._process_response(requests.get(url, headers=self.headers))

    def handle_variable_statement(self, statement):
        self.context[statement.name] = self.with_context(statement.value)

        self.log('variable', statement.name, self.context[statement.name])

    def handle_header_statement(self, statement):
        self.headers[statement.key] = self.with_context(statement.value)

        self.log('header', statement.key, self.headers[statement.key])

    def handle_log_statement(self, statement):
        text = self.with_context_and_headers(statement.text)
        text = text.replace('&#x27;', '"')

        self.log('LOG', statement.tag, '>>>')
        print(text)

    def handle_input_statement(self, statement):
        self.log('INPUT', f'{statement.variable}:', '', end='')
        value = input()
        self.context[statement.variable] = value

    def handle_mode_statement(self, statement):
        if statement.mode == self.mode:
            self.log('MODE', f'{statement.mode}:', 'executing...')
        else:
            # skip statements until next mode.
            self.skip_mode = True

    def load_file(self, file_path):
        parser = Parser(file_path)

        for statement in parser.process():
            self.statements.append(statement)

    def with_context(self, value):
        return pystache.render(value, self.context)

    def with_context_and_headers(self, value):
        context = {}
        context.update(self.context)
        context.update(self.headers)
        return pystache.render(value, context)

    def log(self, verb, bold, rest, end='\n'):
        print(colored(verb.upper().ljust(self.just), 'yellow'), colored(bold, attrs=['bold']), rest, end=end)

    def error(self, rest):
        print(colored('error'.upper().ljust(self.just), 'red', attrs=['bold']), rest)

import json
import os
import sys
import time
from queue import Queue

import pystache
from termcolor import colored

from parser import Parser
from statements import PostStatement, LoadStatement, VariableStatement, SetStatement, GetStatement
import requests


class Postcrypt:
    def __init__(self, main_file):
        self.main_file = main_file

        self.base_path = os.path.dirname(main_file)

        # execution variables.
        self.statements = []
        self.context = {}
        self.headers = {}
        self.last_response = {}

    def process(self):
        self.load_file(file_path=self.main_file)

        # main executor.
        while len(self.statements) != 0:
            statement = self.statements.pop(0)

            self.handle_statement(statement)

    def handle_statement(self, statement):
        if isinstance(statement, LoadStatement):
            self.handle_load_statement(statement)
        elif isinstance(statement, PostStatement):
            self.handle_post_statement(statement)
        elif isinstance(statement, GetStatement):
            self.handle_get_statement(statement)
        elif isinstance(statement, VariableStatement):
            self.handle_variable_statement(statement)
        elif isinstance(statement, SetStatement):
            self.handle_set_statement(statement)

    def handle_load_statement(self, load_statement):
        parser = Parser(os.path.join(self.base_path, load_statement.file_path))

        for statement in parser.process():
            self.statements.insert(0, statement)

    def handle_post_statement(self, statement):
        url = self.with_context(statement.url)
        body = self.with_context(statement.body)

        print(colored('post', 'cyan'), url)

        response = requests.post(url, json=body, headers=self.headers)

        if response.ok:
            self.context['response'] = json.loads(response.text)
        else:
            raise ConnectionError(response.status_code)

    def handle_get_statement(self, statement):
        url = self.with_context(statement.url)

        print(colored('get', 'cyan'), url)

        response = requests.get(url, headers=self.headers)

        if response.ok:
            self.context['response'] = json.loads(response.text)
        else:
            raise ConnectionError(response.status_code)

    def handle_variable_statement(self, statement):
        self.context[statement.name] = self.with_context(statement.value)

        print(colored('variable', 'cyan'), colored(statement.name, attrs=['bold']), self.context[statement.name])

    def handle_set_statement(self, statement):
        self.headers[statement.key] = self.with_context(statement.value)

        print(colored('header', 'cyan'), colored(statement.key, attrs=['bold']), self.headers[statement.key])

    def load_file(self, file_path):
        parser = Parser(file_path)

        for statement in parser.process():
            self.statements.append(statement)

    def with_context(self, value):
        return pystache.render(value, self.context)

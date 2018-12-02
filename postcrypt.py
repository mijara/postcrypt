import json
import os

import pystache
import requests
from termcolor import colored

import handlers
import statements
from input_storage import InputStorage
from logger import Logger
from parser import Parser


class Postcrypt:
    verbs = ['variable', 'request', 'header', 'get']

    def __init__(self, main_file, mode=None, verbose=False, save=False):
        self.main_file = main_file
        self.mode = 'none' if mode is None else mode
        self.verbose = verbose
        self.save = save

        self.base_dir = os.path.dirname(os.path.abspath(main_file))

        self.input_storage = InputStorage(self.base_dir)
        self.logger = Logger(max(len(v) for v in Postcrypt.verbs))

        # saved input values.
        self.saved_input = {} if not save else self.input_storage.initialize()

        self.handlers = {}

        # execution variables.
        self.statements = []
        self.context = {}
        self.headers = {}
        self.last_response = {}
        self.skip_mode = False

    def process(self):
        self.load_file(file_path=self.main_file)

        try:
            self.execute_loop()
            self.log_last_response()

        except requests.exceptions.ConnectionError as e:
            if e.response is not None:
                self.logger.error(f'{e.response.status_code} {e.response.text}')
            else:
                self.logger.error(f'{e.strerror}')

    def execute_loop(self):
        while len(self.statements) != 0:
            statement = self.statements.pop(0)

            if self.skip_mode:
                if isinstance(statement, statements.ModeStatement) and statement.mode == self.mode:
                    self.handle_statement(statement)
                    self.skip_mode = False
            else:
                self.handle_statement(statement)

    def log_last_response(self):
        if 'response' in self.context:
            self.logger.log('response', self.main_file, '>>>')
            print(json.dumps(self.context['response'], indent=2))

    def handle_statement(self, statement):
        self.handlers[statement.__class__](self, statement)

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

    def add_handler(self, clazz, handler):
        self.handlers[clazz] = handler

    def make_default(self):
        self.add_handler(statements.LoadStatement, handlers.handle_load_statement)
        self.add_handler(statements.ModeStatement, handlers.handle_mode_statement)
        self.add_handler(statements.InputStatement, handlers.handle_input_statement)
        self.add_handler(statements.DeleteStatement, handlers.handle_delete_statement)
        self.add_handler(statements.PutStatement, handlers.handle_put_statement)
        self.add_handler(statements.GetStatement, handlers.handle_get_statement)
        self.add_handler(statements.HeaderStatement, handlers.handle_header_statement)
        self.add_handler(statements.LogStatement, handlers.handle_log_statement)
        self.add_handler(statements.PostStatement, handlers.handle_post_statement)
        self.add_handler(statements.VariableStatement, handlers.handle_variable_statement)

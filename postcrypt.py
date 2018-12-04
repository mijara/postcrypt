import inspect
import json
import os
from typing import Type

import requests

import statements
from context import Context
from environment import Environment
from handler import Handler
from handlers.header_handler import HeaderHandler
from handlers.input_handler import InputHandler
from handlers.load_handler import LoadHandler
from handlers.log_handler import LogHandler
from handlers.mode_handler import ModeHandler
from handlers.request_handler import GetRequestHandler, PostRequestHandler, PutRequestHandler, DeleteRequestHandler
from handlers.variable_handler import VariableHandler
from input_storage import InputStorage
from logger import Logger
from parser import Parser
from process_queue import ProcessQueue


class Postcrypt:
    def __init__(self, main_file, mode=None, verbose=False, save=False):
        self.main_file = main_file
        self.mode = 'none' if mode is None else mode
        self.verbose = verbose
        self.save = save

        self.base_dir = os.path.dirname(os.path.abspath(main_file))

        # services.
        self.environment = Environment(self.base_dir)
        self.input_storage = InputStorage(self.base_dir, save)
        self.logger = Logger(16, self.verbose)
        self.process_queue = ProcessQueue(self.mode)
        self.context = Context()

        # handlers for events.
        self.handlers = {}

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
        while self.process_queue.has_next():
            statement = self.process_queue.pop()
            self.handle_statement(statement)

    def log_last_response(self):
        if self.context.has_var('response'):
            self.logger.log('response', self.main_file, '>>>')
            print(json.dumps(self.context.get_var('response'), indent=2))

    def handle_statement(self, statement):
        self.handlers[statement.__class__].handle(statement)

    def load_file(self, file_path):
        parser = Parser(file_path)
        self.process_queue.insert_all(parser.process())

    def add_handler(self, clazz, handler_clazz: Type[Handler]):
        # inject dependencies
        handler = handler_clazz()

        attributes = inspect.getmembers(handler_clazz, lambda a: not (inspect.isroutine(a)))

        required = list(a for a in attributes if a[0] == '__annotations__')

        if len(required) > 0:
            required = required[0][1]
        else:
            required = {}

        for k, v in required.items():
            if v == Context:
                setattr(handler, k, self.context)
            if v == Logger:
                setattr(handler, k, self.logger)
            if v == ProcessQueue:
                setattr(handler, k, self.process_queue)
            if v == InputStorage:
                setattr(handler, k, self.input_storage)
            if v == Environment:
                setattr(handler, k, self.environment)

        self.handlers[clazz] = handler

    def make_default(self):
        self.add_handler(statements.LoadStatement, LoadHandler)
        self.add_handler(statements.ModeStatement, ModeHandler)
        self.add_handler(statements.InputStatement, InputHandler)
        self.add_handler(statements.DeleteStatement, DeleteRequestHandler)
        self.add_handler(statements.PutStatement, PutRequestHandler)
        self.add_handler(statements.GetStatement, GetRequestHandler)
        self.add_handler(statements.PostStatement, PostRequestHandler)
        self.add_handler(statements.HeaderStatement, HeaderHandler)
        self.add_handler(statements.LogStatement, LogHandler)
        self.add_handler(statements.VariableStatement, VariableHandler)

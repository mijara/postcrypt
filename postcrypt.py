import json
import os

import requests

from handlers.input_handler import InputHandler
from handlers.load_handler import LoadHandler
from handlers.mode_handler import ModeHandler
from handlers.variable_handler import VariableHandler
from process_queue import ProcessQueue
from handlers.header_handler import HeaderHandler
from handlers.log_handler import LogHandler
from handlers.request_handler import GetRequestHandler, PostRequestHandler, PutRequestHandler, DeleteRequestHandler
import handlers
import statements
from context import Context
from input_storage import InputStorage
from logger import Logger
from parser import Parser


class Postcrypt:
    def __init__(self, main_file, mode=None, verbose=False, save=False):
        self.main_file = main_file
        self.mode = 'none' if mode is None else mode
        self.verbose = verbose
        self.save = save

        self.base_dir = os.path.dirname(os.path.abspath(main_file))

        self.input_storage = InputStorage(self.base_dir, save)
        self.logger = Logger(16, self.verbose)
        self.process_queue = ProcessQueue(self.mode)

        # handlers for file events.
        self.handlers = {}

        # execution variables.
        self.last_response = {}
        self.skip_mode = False

        self.context = Context()

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

            if self.skip_mode:
                if isinstance(statement, statements.ModeStatement) and statement.mode == self.mode:
                    self.handle_statement(statement)
                    self.skip_mode = False
            else:
                self.handle_statement(statement)

    def log_last_response(self):
        if self.context.has_var('response'):
            self.logger.log('response', self.main_file, '>>>')
            print(json.dumps(self.context.get_var('response'), indent=2))

    def handle_statement(self, statement):
        self.handlers[statement.__class__](self, statement)

    def load_file(self, file_path):
        parser = Parser(file_path)
        self.process_queue.insert_all(parser.process())

    def add_handler(self, clazz, handler):
        self.handlers[clazz] = handler

    def make_default(self):
        get_handler = GetRequestHandler(self.context, self.logger)
        post_handler = PostRequestHandler(self.context, self.logger)
        put_handler = PutRequestHandler(self.context, self.logger)
        delete_handler = DeleteRequestHandler(self.context, self.logger)
        header_handler = HeaderHandler(self.context, self.logger)
        log_handler = LogHandler(self.context, self.logger)
        mode_handler = ModeHandler(self.context, self.logger, self.process_queue)

        variable_handler = VariableHandler(self.context, self.logger)

        load_handler = LoadHandler(self.context, self.logger)
        load_handler.set_process_queue(self.process_queue)
        load_handler.set_base_dir(self.base_dir)

        input_handler = InputHandler(self.context, self.logger, self.input_storage)

        self.add_handler(statements.LoadStatement, lambda x, y: load_handler.handle(y))
        self.add_handler(statements.ModeStatement, lambda x, y: mode_handler.handle(y))
        self.add_handler(statements.InputStatement, lambda x, y: input_handler.handle(y))
        self.add_handler(statements.DeleteStatement, lambda x, y: delete_handler.handle(y))
        self.add_handler(statements.PutStatement, lambda x, y: put_handler.handle(y))
        self.add_handler(statements.GetStatement, lambda x, y: get_handler.handle(y))
        self.add_handler(statements.PostStatement, lambda x, y: post_handler.handle(y))
        self.add_handler(statements.HeaderStatement, lambda x, y: header_handler.handle(y))
        self.add_handler(statements.LogStatement, lambda x, y: log_handler.handle(y))
        self.add_handler(statements.VariableStatement, lambda x, y: variable_handler.handle(y))

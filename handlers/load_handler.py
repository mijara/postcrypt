import os

from handler import Handler
from parser import Parser


class LoadHandler(Handler):
    def __init__(self, context, logger):
        super().__init__(context, logger)
        self.process_queue = None
        self._base_dir = None

    def handle(self, statement):
        parser = Parser(os.path.join(self._base_dir, statement.file_path))
        statements = parser.process()
        self.process_queue.insert_all(statements)

        if self.logger.verbose:
            self.logger.log('LOAD', statement.file_path, f'{len(statements)} statement(s)')

    def set_process_queue(self, process_queue):
        self.process_queue = process_queue

    def set_base_dir(self, base_dir):
        self._base_dir = base_dir

import os

from environment import Environment
from handler import Handler
from logger import Logger
from parser import Parser
from process_queue import ProcessQueue


class LoadHandler(Handler):
    process_queue: ProcessQueue
    environment: Environment
    logger: Logger

    def handle(self, statement):
        parser = Parser(os.path.join(self.environment.base_dir, statement.file_path))
        statements = parser.process()
        self.process_queue.insert_all(statements)

        if self.logger.verbose:
            self.logger.log('LOAD', statement.file_path, f'{len(statements)} statement(s)')

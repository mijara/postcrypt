import os

from services.environment import Environment
from handlers.handler import Handler
from services.logger import Logger
from parser import Parser
from services.process_queue import ProcessQueue


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

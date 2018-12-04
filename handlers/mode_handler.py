from handlers.handler import Handler
from services.logger import Logger
from services.process_queue import ProcessQueue


class ModeHandler(Handler):
    process_queue: ProcessQueue
    logger: Logger

    def handle(self, statement):
        if statement.mode == self.process_queue.mode:
            if self.logger.verbose:
                self.logger.log('MODE', f'{statement.mode}:', 'executing...')
        else:
            self.process_queue.skip_mode()

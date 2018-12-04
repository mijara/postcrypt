from handler import Handler
from logger import Logger
from process_queue import ProcessQueue


class ModeHandler(Handler):
    process_queue: ProcessQueue
    logger: Logger

    def handle(self, statement):
        if statement.mode == self.process_queue.mode:
            if self.logger.verbose:
                self.logger.log('MODE', f'{statement.mode}:', 'executing...')
        else:
            self.process_queue.skip_mode()

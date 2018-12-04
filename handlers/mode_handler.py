from handler import Handler
from process_queue import ProcessQueue


class ModeHandler(Handler):
    def __init__(self, context, logger, process_queue):
        super().__init__(context, logger)

        self.process_queue: ProcessQueue = process_queue

    def handle(self, statement):
        if statement.mode == self.process_queue.mode:
            if self.logger.verbose:
                self.logger.log('MODE', f'{statement.mode}:', 'executing...')
        else:
            self.process_queue.skip_mode()

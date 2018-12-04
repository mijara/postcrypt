from context import Context
from handler import Handler
from logger import Logger


class HeaderHandler(Handler):
    logger: Logger
    context: Context

    def handle(self, statement):
        self.context.set_header(statement.key, self.context.render(statement.value))

        if self.logger.verbose:
            self.logger.log('header', statement.key, self.context.get_header(statement.key))

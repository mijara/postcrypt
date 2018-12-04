from services.context import Context
from handlers.handler import Handler
from services.logger import Logger


class VariableHandler(Handler):
    logger: Logger
    context: Context

    def handle(self, statement):
        self.context.set_var(statement.name, self.context.render(statement.value))

        if self.logger.verbose:
            self.logger.log('variable', statement.name, self.context.get_var(statement.name))

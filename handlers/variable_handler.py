from context import Context
from handler import Handler
from logger import Logger


class VariableHandler(Handler):
    logger: Logger
    context: Context

    def handle(self, statement):
        self.context.set_var(statement.name, self.context.render(statement.value))

        if self.logger.verbose:
            self.logger.log('variable', statement.name, self.context.get_var(statement.name))

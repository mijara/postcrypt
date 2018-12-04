from handler import Handler


class VariableHandler(Handler):
    def handle(self, statement):
        self.context.set_var(statement.name, self.context.render(statement.value))

        if self.logger.verbose:
            self.logger.log('variable', statement.name, self.context.get_var(statement.name))

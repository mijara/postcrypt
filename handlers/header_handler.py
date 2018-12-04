from handler import Handler


class HeaderHandler(Handler):
    def handle(self, statement):
        self.context.set_header(statement.key, self.context.render(statement.value))

        if self.logger.verbose:
            self.logger.log('header', statement.key, self.context.get_header(statement.key))

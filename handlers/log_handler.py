from context import Context
from handler import Handler
from logger import Logger


class LogHandler(Handler):
    logger: Logger
    context: Context

    def handle(self, statement):
        text = self.context.render_with_headers(statement.text)
        text = text.replace('&#x27;', '"')

        self.logger.log('LOG', statement.tag, '>>>')
        print(text)

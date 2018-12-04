from handler import Handler


class LogHandler(Handler):
    def handle(self, statement):
        text = self.context.render_with_headers(statement.text)
        text = text.replace('&#x27;', '"')

        self.logger.log('LOG', statement.tag, '>>>')
        print(text)

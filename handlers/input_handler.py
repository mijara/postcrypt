from handler import Handler
from input_storage import InputStorage


class InputHandler(Handler):
    def __init__(self, context, logger, input_storage):
        super().__init__(context, logger)
        self.input_storage: InputStorage = input_storage

    def handle(self, statement):
        if self.input_storage.has_input(statement.variable):
            self.logger.log('INPUT', f'{statement.variable}', f'[{self.input_storage.get_input(statement.variable)}]: ', end='')
            value = input()

            if value == '':
                value = self.input_storage.get_input(statement.variable)
        else:
            self.logger.log('INPUT', f'{statement.variable}:', '', end='')
            value = input()

        self.context.set_var(statement.variable, value)
        self.input_storage.set_input(statement.variable, value)

from context import Context
from handler import Handler
from input_storage import InputStorage
from logger import Logger


class InputHandler(Handler):
    context: Context
    logger: Logger
    input_storage: InputStorage

    def handle(self, statement):
        if self.input_storage.has_input(statement.variable):
            self.logger.log(
                'INPUT', f'{statement.variable}',
                f'[{self.input_storage.get_input(statement.variable)}]: ',
                end=''
            )

            value = input()

            if value == '':
                value = self.input_storage.get_input(statement.variable)
        else:
            self.logger.log('INPUT', f'{statement.variable}:', '', end='')
            value = input()

        self.context.set_var(statement.variable, value)
        self.input_storage.set_input(statement.variable, value)

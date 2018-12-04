from statements import ModeStatement


class ProcessQueue:
    def __init__(self, mode):
        self.statements = []
        self.mode = mode

    def has_next(self):
        return len(self.statements) > 0

    def pop(self):
        return self.statements.pop(0)

    def insert_all(self, statements):
        for i in range(len(statements) - 1, -1, -1):
            self.statements.insert(0, statements[i])

    def insert(self, statement):
        self.statements.insert(0, statement)

    def skip_mode(self):
        while self.has_next():
            statement = self.pop()

            if isinstance(statement, ModeStatement):
                self.insert(statement)
                break

from abc import ABC


class Handler(ABC):
    def handle(self, statement):
        raise NotImplementedError()

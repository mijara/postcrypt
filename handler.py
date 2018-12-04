from abc import ABC

from context import Context
from logger import Logger


class Handler(ABC):
    def __init__(self, context, logger):
        self.context: Context = context
        self.logger: Logger = logger

    def handle(self, statement):
        raise NotImplementedError()

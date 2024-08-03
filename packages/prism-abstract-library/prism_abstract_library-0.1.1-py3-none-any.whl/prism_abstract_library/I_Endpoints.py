from fastapi import FastAPI
from abc import ABC, abstractmethod


class IEndpoints(ABC):
    @abstractmethod
    def __init__(self, app: FastAPI):
        """Initialise endpoints handler"""

        pass

    @abstractmethod
    def handle(self):
        """Handle endpoints"""

        pass

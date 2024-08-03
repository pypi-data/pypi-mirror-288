from fastapi import FastAPI
from abc import ABC, abstractmethod
from typing import Type


class IAPI(ABC):
    @abstractmethod
    def __init__(self, api: Type[FastAPI]):
        """Initialise the API."""

        pass

    @abstractmethod
    def routes(self):
        """Define the routes for the API."""

        pass

from abc import ABC, abstractmethod


class ITable(ABC):
    @abstractmethod
    def __init__(self, table_name: str):

        pass

from sqlalchemy.orm import Session
from abc import ABC, abstractmethod


class IDatabase(ABC):
    @abstractmethod
    def __init__(self, db: Session):
        """Database initialization."""

        pass

    @abstractmethod
    def create_all_tables(self):
        """Creates all tables in the database."""

        pass

    @abstractmethod
    def drop_all_tables(self):
        """Drops all tables in the database."""

        pass

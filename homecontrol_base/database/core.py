from contextlib import contextmanager
from typing import Any, Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from homecontrol_base.config.database import DatabaseConfig


class Database:
    """Class for handling connections to a database"""

    _name: str
    _engine: Engine
    _session: Any
    _declarative_base: Any

    def __init__(
        self, name: str, declarative_base: Any, config: DatabaseConfig
    ) -> None:
        """Construct a database

        Args:
            name (str): Name of the database
            config (DatabaseConfig): Database config
        """

        self._name = name
        self._engine = create_engine(config.get_url(self._name))
        self._session = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )
        self._declarative_base = declarative_base

    def create_tables(self):
        """Creates all of the tables within this database"""
        self._declarative_base.metadata.create_all(bind=self._engine)

    @contextmanager
    def connect(self) -> Generator[Session, None, None]:
        session = self._session()
        try:
            yield session
        finally:
            session.close()

    @property
    def engine(self):
        return self._engine

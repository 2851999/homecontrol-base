from contextlib import contextmanager
from typing import Any, Generator, Generic, TypeVar

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from homecontrol_base.config.database import DatabaseConfig


class DatabaseConnection:
    """Class for handling a connection to a database"""

    _session: Session

    def __init__(self, session: Session):
        """Constructor

        Args:
            session (Session): Database session to use
        """

        self._session = session


TDatabaseConnection = TypeVar("TDatabaseConnection", bound=DatabaseConnection)


class Database(Generic[TDatabaseConnection]):
    """Class for handling connections to a database"""

    _name: str
    _engine: Engine
    _session_factory: Any
    _declarative_base: Any
    _connection_type: TDatabaseConnection

    def __init__(
        self,
        name: str,
        declarative_base: Any,
        connection_type: TDatabaseConnection,
        config: DatabaseConfig,
    ) -> None:
        """Construct a database

        Args:
            name (str): Name of the database
            declarative_base (Any): Declarative base used in all models
                                    of the database
            connection_type (TDatabaseConnection): Type of connection returned
                                    after connecting to the database (good place
                                    for functions for performing specific
                                    operations on the database)
            config (DatabaseConfig): Database config
        """

        self._name = name
        self._engine = create_engine(config.get_url(self._name))
        self._session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )
        self._declarative_base = declarative_base
        self._connection_type = connection_type

    def create_tables(self):
        """Creates all of the tables within this database"""
        self._declarative_base.metadata.create_all(bind=self._engine)

    @contextmanager
    def connect(self) -> Generator[TDatabaseConnection, None, None]:
        """Connects to the database"""
        session = self._session_factory()
        try:
            yield self._connection_type(session)
        finally:
            session.close()

    @property
    def engine(self):
        return self._engine

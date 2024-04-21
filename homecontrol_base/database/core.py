from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, Generic, Type, TypeVar

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

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
    _connection_type: Type[TDatabaseConnection]

    def __init__(
        self,
        name: str,
        declarative_base: Any,
        connection_type: Type[TDatabaseConnection],
        config: DatabaseConfig,
        alembic_config_path: Path,
    ) -> None:
        """Construct a database

        Args:
            name (str): Name of the database (Will create if doesn't already exist)
            declarative_base (Any): Declarative base used in all models
                                    of the database
            connection_type (TDatabaseConnection): Type of connection returned
                                    after connecting to the database (good place
                                    for functions for performing specific
                                    operations on the database)
            config (DatabaseConfig): Database config
            alembic_config_path (Path): Path to alembic config (for stamping initial database version)
        """

        self._name = name

        # Create database if it doesn't exist in case not using sqlite
        url = config.get_url(self._name)
        does_database_exist = database_exists(url)
        if not does_database_exist:
            create_database(url)

        self._engine = create_engine(config.get_url(self._name))
        self._session_factory = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )
        self._declarative_base = declarative_base
        self._connection_type = connection_type

        # Create the tables if they starting for first time
        if not does_database_exist:
            # Create all tables
            self._declarative_base.metadata.create_all(bind=self._engine)

            # Mark this version as head for future migrations
            alembic_config = Config(alembic_config_path)
            command.stamp(alembic_config, "head")

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

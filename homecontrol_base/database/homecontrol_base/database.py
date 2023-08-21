from sqlalchemy.orm import Session

from homecontrol_base.config.database import DatabaseConfig
from homecontrol_base.database.core import Database, DatabaseConnection
from homecontrol_base.database.homecontrol_base.models import Base


class HomecontrolBaseDatabaseConnection(DatabaseConnection):
    """Class for handling a connection to the homecontrol-base database"""

    def __init__(self, session: Session):
        super().__init__(session)


class HomecontrolBaseDatabase(Database[HomecontrolBaseDatabaseConnection]):
    """Database for storing information handled by homecontrol-base"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(
            "homecontrol_base", Base, HomecontrolBaseDatabaseConnection, config
        )


database = HomecontrolBaseDatabase(DatabaseConfig())

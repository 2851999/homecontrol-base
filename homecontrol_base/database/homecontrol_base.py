from typing import Any
from sqlalchemy.orm import declarative_base
from homecontrol_base.config.database import DatabaseConfig

from homecontrol_base.database.core import Database

Base = declarative_base()


class HomecontrolBaseDatabase(Database):
    """Database for storing information handled by homecontrol-base"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__("homecontrol_base", Base, config)


db = HomecontrolBaseDatabase(DatabaseConfig())

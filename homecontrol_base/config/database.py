from typing import Optional

from pydantic.dataclasses import dataclass
from sqlalchemy import URL

from homecontrol_base.config.base import BaseConfig


@dataclass
class DatabaseConfigData:
    """Database connection info"""

    driver: str
    username: Optional[str]
    password: Optional[str]
    host: Optional[str]
    port: Optional[int]


class DatabaseConfig(BaseConfig[DatabaseConfigData]):
    """All database config"""

    def __init__(self) -> None:
        super().__init__("database.json", DatabaseConfigData)

    def get_url(self, database_name: str) -> URL:
        """Returns a URL for connecting to a particular database"""
        if self._data.driver == "sqlite":
            database_name += ".db"

        return URL.create(
            drivername=self._data.driver,
            username=self._data.username,
            password=self._data.password,
            host=self._data.host,
            port=self._data.port,
            database=database_name,
        )

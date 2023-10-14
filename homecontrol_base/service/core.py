from typing import Generic

from homecontrol_base.database.core import TDatabaseConnection


class BaseService(Generic[TDatabaseConnection]):
    """Used for handling a database connection over a longer period of time
    e.g. during a REST API endpoint execution"""

    _db_conn: TDatabaseConnection

    def __init__(self, database_connection: TDatabaseConnection) -> None:
        self._db_conn = database_connection

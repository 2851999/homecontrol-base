from typing import Generic

from homecontrol_base.database.core import TDatabaseConnection


class BaseService(Generic[TDatabaseConnection]):
    """Used for handling a database connection over a longer period of time
    e.g. during a REST API endpoint execution"""

    db_conn: TDatabaseConnection

    def __init__(self, db_conn: TDatabaseConnection) -> None:
        self.db_conn = db_conn

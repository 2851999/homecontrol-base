from sqlalchemy.orm import Session

from homecontrol_base.config.database import DatabaseConfig
from homecontrol_base.database.core import Database, DatabaseConnection
from homecontrol_base.database.homecontrol_base.ac_device import ACDevicesDBConnection
from homecontrol_base.database.homecontrol_base.broadlink_actions import (
    BroadlinkActionInDBsDBConnection,
)
from homecontrol_base.database.homecontrol_base.broadlink_devices import (
    BroadlinkDevicesDBConnection,
)
from homecontrol_base.database.homecontrol_base.hue_bridges import (
    HueBridgesDBConnection,
)
from homecontrol_base.database.homecontrol_base.models import Base


class HomecontrolBaseDatabaseConnection(DatabaseConnection):
    """Class for handling a connection to the homecontrol-base database"""

    ac_devices: ACDevicesDBConnection
    hue_bridges: HueBridgesDBConnection
    broadlink_devices: BroadlinkDevicesDBConnection
    broadlink_actions: BroadlinkActionInDBsDBConnection

    def __init__(self, session: Session):
        super().__init__(session)

        self.ac_devices = ACDevicesDBConnection(session)
        self.hue_bridges = HueBridgesDBConnection(session)
        self.broadlink_devices = BroadlinkDevicesDBConnection(session)
        self.broadlink_actions: BroadlinkActionInDBsDBConnection(session)


class HomecontrolBaseDatabase(Database[HomecontrolBaseDatabaseConnection]):
    """Database for storing information handled by homecontrol-base"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(
            "homecontrol_base", Base, HomecontrolBaseDatabaseConnection, config
        )


database = HomecontrolBaseDatabase(DatabaseConfig())

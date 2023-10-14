from typing import Optional

from sqlalchemy.orm import Session

from homecontrol_base.config.database import DatabaseConfig
from homecontrol_base.database.core import Database, DatabaseConnection
from homecontrol_base.database.homecontrol_base.ac_device import ACDevicesDBConnection
from homecontrol_base.database.homecontrol_base.broadlink_actions import (
    BroadlinkActionDBConnection,
)
from homecontrol_base.database.homecontrol_base.broadlink_devices import (
    BroadlinkDevicesDBConnection,
)
from homecontrol_base.database.homecontrol_base.hue_bridges import (
    HueBridgesDBConnection,
)
from homecontrol_base.database.homecontrol_base.models import Base


class HomeControlBaseDatabaseConnection(DatabaseConnection):
    """Class for handling a connection to the homecontrol-base database"""

    _ac_devices: Optional[ACDevicesDBConnection] = None
    _hue_bridges: Optional[HueBridgesDBConnection] = None
    _broadlink_devices: Optional[BroadlinkDevicesDBConnection] = None
    _broadlink_actions: Optional[BroadlinkActionDBConnection] = None

    def __init__(self, session: Session):
        super().__init__(session)

    @property
    def ac_devices(self):
        if not self._ac_devices:
            self._ac_devices = ACDevicesDBConnection(self._session)
        return self._ac_devices

    @property
    def hue_bridges(self):
        if not self._hue_bridges:
            self._hue_bridges = HueBridgesDBConnection(self._session)
        return self._hue_bridges

    @property
    def broadlink_devices(self):
        if not self._broadlink_devices:
            self._broadlink_devices = BroadlinkDevicesDBConnection(self._session)
        return self._broadlink_devices

    @property
    def broadlink_actions(self):
        if not self._broadlink_actions:
            self._broadlink_actions = BroadlinkActionDBConnection(self._session)
        return self._broadlink_actions


class HomeControlBaseDatabase(Database[HomeControlBaseDatabaseConnection]):
    """Database for storing information handled by homecontrol-base"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(
            "homecontrol_base", Base, HomeControlBaseDatabaseConnection, config
        )


database = HomeControlBaseDatabase(DatabaseConfig())

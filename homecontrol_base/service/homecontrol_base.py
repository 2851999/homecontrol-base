from contextlib import contextmanager
from typing import Optional

from homecontrol_base.aircon.manager import ACManager
from homecontrol_base.aircon.service import ACService
from homecontrol_base.broadlink.manager import BroadlinkManager
from homecontrol_base.broadlink.service import BroadlinkService
from homecontrol_base.database.homecontrol_base.database import (
    HomeControlBaseDatabaseConnection,
)
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)
from homecontrol_base.hue.manager import HueManager
from homecontrol_base.hue.service import HueService
from homecontrol_base.service.core import BaseService


class HomeControlBaseService(BaseService[HomeControlBaseDatabaseConnection]):
    """Service for homecontrol_base"""

    _ac_manager: Optional[ACManager]
    _aircon: Optional[ACService] = None
    _hue_manager: Optional[HueManager]
    _hue: Optional[HueService] = None
    _broadlink_manager: Optional[BroadlinkManager]
    _broadlink: Optional[BroadlinkService] = None

    def __init__(
        self,
        database_connection: HomeControlBaseDatabaseConnection,
        ac_manager: Optional[ACManager] = None,
        hue_manager: Optional[HueManager] = None,
        broadlink_manager: Optional[BroadlinkManager] = None,
    ):
        super().__init__(database_connection)

        self._ac_manager = ac_manager
        self._hue_manager = hue_manager
        self._broadlink_manager = broadlink_manager

    # Below are properties that create the sub services when required

    @property
    def aircon(self) -> ACService:
        if not self._aircon:
            if not self._ac_manager:
                self._ac_manager = ACManager()
            self._aircon = ACService(db_conn=self._db_conn, ac_manager=self._ac_manager)
        return self._aircon

    @property
    def hue(self) -> HueService:
        if not self._hue:
            if not self._hue_manager:
                self._hue_manager = HueManager()
            self._hue = HueService(db_conn=self._db_conn, hue_manager=self._hue_manager)
        return self._hue

    @property
    def broadlink(self) -> BroadlinkService:
        if not self._broadlink:
            if not self._broadlink_manager:
                self._broadlink_manager = BroadlinkManager()
            self._broadlink = BroadlinkService(
                db_conn=self._db_conn, broadlink_manager=self._broadlink_manager
            )
        return self._broadlink


@contextmanager
def create_homecontrol_base_service(
    ac_manager: Optional[ACManager] = None,
    hue_manager: Optional[HueManager] = None,
    broadlink_manager: Optional[BroadlinkManager] = None,
):
    with homecontrol_db.connect() as conn:
        yield HomeControlBaseService(
            conn,
            ac_manager=ac_manager,
            hue_manager=hue_manager,
            broadlink_manager=broadlink_manager,
        )

from homecontrol_base.config.hue import HueConfig
from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.database.homecontrol_base.database import (
    HomeControlBaseDatabaseConnection,
)
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_base_db,
)
from homecontrol_base.hue.bridge import HueBridge


class HueManager:
    """Manages a set of Hue bridge instances"""

    _hue_config: HueConfig
    _bridges: dict[str, HueBridge]

    def __init__(self):
        self._hue_config = HueConfig()
        self._bridges = {}

        self._load_all()

    def _load_bridge(self, bridge_info: models.HueBridgeInDB) -> HueBridge:
        """Adds a bridge into _bridges"""
        bridge = HueBridge(bridge_info, self._hue_config)
        self._bridges[bridge_info.id] = bridge
        return bridge

    def _load_all(self):
        with homecontrol_base_db.connect() as conn:
            bridges = conn.hue_bridges.get_all()
            for bridge_info in bridges:
                self._load_bridge(bridge_info)

    def get_bridge(
        self, db_conn: HomeControlBaseDatabaseConnection, bridge_id: str
    ) -> HueBridge:
        """Returns a bridge given its id

        Attempts to load from the database if not already loaded

        Args:
            db_conn (HomeControlBaseDatabaseConnection): Database connection
                    to use in the event a device needs to be looked up
            bridge_id (str): ID of the bridge to get

        Raises:
            DeviceNotFoundError: If the bridge isn't found
        """
        bridge = self._bridges.get(bridge_id)

        if not bridge:
            # Attempt to load it
            bridge = self._load_bridge(db_conn.hue_bridges.get(bridge_id))
        return bridge

    def add_bridge(self, bridge_info: models.HueBridgeInDB) -> HueBridge:
        """Adds a Hue bridge

        Args:
            bridge_info (models.HueBridgeInDB): Bridge info

        Raises:
            HueBridgeButtonNotPressedError: When the button on the Hue bridge
                                            needs to be pressed
        """
        return self._load_bridge(bridge_info)

    def remove_bridge(self, bridge_id: str) -> None:
        """Removes the bridge with the given ID (including from the database)

        Args:
            bridge_id (str): ID of the bridge to remove

        Raises:
            DeviceNotFoundError: When the device isn't found
        """
        # Delete from the database
        with homecontrol_base_db.connect() as conn:
            conn.hue_bridges.delete(bridge_id)
        # Remove from manager if already loaded
        if bridge_id in self._bridges:
            del self._bridges[bridge_id]

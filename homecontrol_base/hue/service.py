from typing import Callable

from homecontrol_base.database.homecontrol_base.database import (
    HomeControlBaseDatabaseConnection,
)
from homecontrol_base.hue.bridge import HueBridge
from homecontrol_base.hue.exceptions import HueBridgeButtonNotPressedError
from homecontrol_base.hue.manager import HueManager
from homecontrol_base.hue.structs import HueBridgeDiscoverInfo
from homecontrol_base.service.core import BaseService


class HueService(BaseService[HomeControlBaseDatabaseConnection]):
    """Service for handling Hue bridges"""

    _hue_manager: HueManager

    def __init__(
        self,
        db_conn: HomeControlBaseDatabaseConnection,
        hue_manager: HueManager,
    ):
        super().__init__(db_conn)

        self._hue_manager = hue_manager

    def get_bridge(self, device_id: str) -> HueBridge:
        """Returns a bridge given its id

        Attempts to load from the database if not already loaded

        Args:
            bridge_id (str): ID of the bridge to get

        Raises:
            DeviceNotFoundError: If the bridge isn't found
        """
        return self._hue_manager.get_device(db_conn=self._db_conn, device_id=device_id)

    def get_bridge_by_name(self, bridge_name: str) -> HueBridge:
        """Returns a bridge given its name - slower than get_bridge

        Attempts to load from the database if not already loaded

        Args:
            bridge_name (str): The name of the bridge to get

        Raises:
            DeviceNotFoundError: If the bridge isn't found
        """
        # Look up the device in the database (so can get id)
        bridge_info = self._db_conn.hue_bridges.get_by_name(bridge_name)
        return self._hue_manager.get_bridge(
            db_conn=self._db_conn, bridge_id=str(bridge_info.id)
        )

    def add_bridge(self, name: str, discover_info: HueBridgeDiscoverInfo) -> HueBridge:
        """Adds a Hue bridge

        Args:
            name (str): Name to label the bridge
            discover_info (HueBridgeDiscoverInfo): Bridge info from discovery

        Raises:
            HueBridgeButtonNotPressedError: When the button on the Hue bridge
                                            needs to be pressed
        """
        bridge_info = HueBridge.authenticate(
            name=name,
            discover_info=discover_info,
            ca_cert=self._hue_manager._hue_config.ca_cert,
        )
        bridge_info = self._db_conn.hue_bridges.create(bridge_info)
        return self._hue_manager.add_bridge(bridge_info=bridge_info)

    def discover(self) -> list[HueBridgeDiscoverInfo]:
        """Attempts to discover all Hue bridges on the network"""
        return HueBridge.discover(self._hue_manager._hue_config.mDNS_discovery)

    def discover_and_add_all_bridges(
        self,
        name_function: Callable[
            [int, HueBridgeDiscoverInfo], str
        ] = lambda i, discover_info: f"Bridge{i}",
    ):
        """Discovers and adds all bridges found on the network

        This will pause by requiring input via command line to confirm
        all buttons on the bridges have been pressed. Should only be
        called once. (Utility method only)

        Args:
            name_function (Callable[[int], str]): Function that should
                          return the name of a bridge given it's index
                          and HueBridgeDiscoverInfo
        """
        # Find all available bridges
        discovered_bridges = self.discover()
        done = [False] * len(discovered_bridges)
        while not all(done):
            for index, discovered_bridge in enumerate(discovered_bridges):
                if not done[index]:
                    try:
                        self.add_bridge(
                            name_function(index, discovered_bridge), discovered_bridge
                        )
                        done[index] = True
                    except HueBridgeButtonNotPressedError:
                        pass
            if not all(done):
                input(
                    "Please press the button on top of all your Hue bridge's and then press enter"
                )

    def remove_bridge(self, bridge_id: str) -> None:
        """Removes a Hue bridge

        Args:
            bridge_id (str): ID of the bridge to remove

        Raises:
            DeviceNotFoundError: When the bridge isn't found
        """
        self._hue_manager.remove_bridge(bridge_id)

from typing import Callable

from homecontrol_base.config.hue import HueConfig
from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)
from homecontrol_base.hue.bridge import HueBridge
from homecontrol_base.hue.exceptions import HueBridgeButtonNotPressedError
from homecontrol_base.hue.structs import HueBridgeDiscoverInfo


class HueManager:
    """Manages a set of Hue bridge instances"""

    _hue_config: HueConfig
    _bridges: dict[str, HueBridge]

    def __init__(self):
        self._hue_config = HueConfig()
        self._bridges = {}

        self._load_all()

    def _load_bridge(self, bridge_info: models.HueBridgeInfo) -> HueBridge:
        """Adds a bridge into _bridges"""
        bridge = HueBridge(bridge_info)
        self._bridges[bridge_info.id] = bridge
        return bridge

    def _load_all(self):
        with homecontrol_db.connect() as conn:
            bridges = conn.get_hue_bridges()
            for bridge_info in bridges:
                self._load_bridge(bridge_info)

    def get_bridge(self, bridge_id: str) -> HueBridge:
        """Returns a bridge given its id

        Attempts to load from the database if not already loaded

        Args:
            bridge_id (str): ID of the bridge to get

        Raises:
            DeviceNotFoundError: If the bridge isn't found
        """
        bridge = self._bridges.get(bridge_id)

        if not bridge:
            # Attempt to load it
            with homecontrol_db.connect() as conn:
                bridge = self._load_bridge(conn.get_hue_bridge(bridge_id))
        return bridge

    def get_bridge_by_name(self, bridge_name: str) -> HueBridge:
        """Returns a bridge given its name - slower than get_bridge

        Attempts to load from the database if not already loaded

        Args:
            bridge_name (str): The name of the bridge to get

        Raises:
            DeviceNotFoundError: If the bridge isn't found
        """
        # Look up the bridge in the database (so can get id)
        with homecontrol_db.connect() as conn:
            bridge_info = conn.get_hue_bridge_by_name(bridge_name)
        bridge = self._devices.get(bridge_info.id)
        if not bridge:
            bridge = self._load_bridge(bridge_info)
        return bridge

    def add_bridge(self, name: str, discover_info: HueBridgeDiscoverInfo) -> HueBridge:
        """Adds a Hue bridge

        Args:
            discover_info (HueBridgeDiscoverInfo): Bridge info from discovery

        Raises:
            HueBridgeButtonNotPressedError: When the button on the Hue bridge
                                            needs to be pressed
        """
        bridge_info = HueBridge.authenticate(
            name=name,
            discover_info=discover_info,
            ca_cert=self._hue_config.ca_cert,
        )
        with homecontrol_db.connect() as conn:
            bridge_info = conn.create_hue_bridge(bridge_info)
        return self._load_bridge(bridge_info)

    def discover(self) -> list[HueBridgeDiscoverInfo]:
        """Attempts to discover all Hue bridges on the network"""
        return HueBridge.discover(self._hue_config.mDNS_discovery)

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

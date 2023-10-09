from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from homecontrol_base.config.hue import HueConfig
from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.hue.api.connection import HueBridgeAPIConnection
from homecontrol_base.hue.discovery import discover_hue_bridges
from homecontrol_base.hue.session import HueBridgeSession
from homecontrol_base.hue.structs import HueBridgeDiscoverInfo


class HueBridge:
    """Handles a Phillips Hue bridge"""

    _bridge_info: models.HueBridgeInDB
    _hue_config: HueConfig

    def __init__(
        self, bridge_info: models.HueBridgeInDB, hue_config: HueConfig
    ) -> None:
        """Constructor

        Args:
            bridge_info (models.HueBridgeInDB): Hue bridge connection info
            hue_config (HueConfig): Hue config
        """
        self._bridge_info = bridge_info
        self._hue_config = hue_config

    @contextmanager
    def connect_api(self) -> Generator[HueBridgeAPIConnection, None, None]:
        with HueBridgeSession(
            connection_info=self._bridge_info, ca_cert=self._hue_config.ca_cert
        ) as session:
            yield HueBridgeAPIConnection(session)

    @staticmethod
    def authenticate(
        name: str, discover_info: HueBridgeDiscoverInfo, ca_cert: Path
    ) -> models.HueBridgeInDB:
        """Requests a new application key from a bridge

        When first run, will produce an error requesting the user to press
        the button to confirm authentication. The second time this is called
        authentication should be successful.

        Args:
            name (str): Name to label the bridge
            discover_info (str): Information from discovery
            ca_cert (Path): Path to the Hue bridge certificate required for a
                            HTTPS connection

        Returns:
            models.HueBridgeInDB: Information required to connect to a bride

        Raises:
            HueBridgeButtonNotPressedError: When the button on the Hue bridge
                                            needs to be pressed
        """
        with HueBridgeSession(
            connection_info=discover_info, ca_cert=ca_cert
        ) as session:
            conn = HueBridgeAPIConnection(session)
            return conn.authenticate(name)

    @staticmethod
    def discover(mDNS_discovery: bool) -> list[HueBridgeDiscoverInfo]:
        """Discovers all Phillip's Hue bridges that are available on the
        current network

        Args:
            mDNS_discovery (bool): Whether to use mDNS for discovery
        """

        return discover_hue_bridges(mDNS_discovery)

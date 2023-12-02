import time

import requests
from pydantic import TypeAdapter
from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
from homecontrol_base.hue.exceptions import HueBridgesDiscoveryError

from homecontrol_base.hue.structs import HueBridgeDiscoverInfo

DISCOVER_URL = "https://discovery.meethue.com/"


class HueDiscoveryListener(ServiceListener):
    """Listener for Hue bridges"""

    _found_devices: list[HueBridgeDiscoverInfo]

    def __init__(self, **args):
        super().__init__(**args)
        self._found_devices = []

    def update_service(self, zeroconf: Zeroconf, type_: str, name: str) -> None:
        pass

    def remove_service(self, zeroconfc: Zeroconf, type_: str, name: str) -> None:
        pass

    def add_service(self, zeroconf: Zeroconf, type_: str, name: str) -> None:
        info = zeroconf.get_service_info(type_, name)
        self._found_devices.append(
            HueBridgeDiscoverInfo(
                id=info.properties[b"bridgeid"],
                internalipaddress=info.parsed_addresses()[0],
                port=info.port,
            )
        )

    def get_found_devices(self) -> list[HueBridgeDiscoverInfo]:
        return self._found_devices


def discover_hue_bridges(mDNS_discovery: bool) -> list[HueBridgeDiscoverInfo]:
    """Discovers all Phillips Hue bridges that are available on the
    current network

    Args:
        mDNS_discovery (bool): Whether to use mDNS for discovery

    Raises:
        HueBridgesDiscoveryError: When not using mDNS but getting rate limited
    """
    if mDNS_discovery:
        zeroconf = Zeroconf()
        listener = HueDiscoveryListener()
        browser = ServiceBrowser(zeroconf, "_hue._tcp.local.", listener)
        # Wait 5 seconds to collect as many as possible
        time.sleep(5)
        zeroconf.close()
        return listener.get_found_devices()
    else:
        response = requests.get(DISCOVER_URL)
        if response.status_code == 429:
            raise HueBridgesDiscoveryError(response.reason)
        response.raise_for_status()
        bridges = TypeAdapter(list[HueBridgeDiscoverInfo]).validate_python(
            response.json()
        )
        return bridges

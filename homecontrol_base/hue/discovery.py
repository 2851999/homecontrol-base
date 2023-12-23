import asyncio

import requests
from pydantic import TypeAdapter
from zeroconf import ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf

from homecontrol_base.hue.exceptions import HueBridgesDiscoveryError
from homecontrol_base.hue.structs import HueBridgeDiscoverInfo

DISCOVER_URL = "https://discovery.meethue.com/"


class HueDiscoveryListener:
    """Listener for Hue bridges"""

    _found_devices: list[HueBridgeDiscoverInfo]

    def __init__(self, **args):
        super().__init__(**args)
        self._found_devices = []

    async def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Called when service is first discovered"""

        info = AsyncServiceInfo(type_, name)
        await info.async_request(zc, 3000)
        self._found_devices.append(
            HueBridgeDiscoverInfo(
                id=info.properties[b"bridgeid"],
                internalipaddress=info.parsed_addresses()[0],
                port=info.port,
            )
        )

    def get_service_handler(self):
        """Returns an asynchronous handler to be called when a service state
        changes (To be passed to AsyncServiceBrowser)

        See https://github.com/python-zeroconf/python-zeroconf/blob/master/examples/async_browser.py
        """

        def async_on_service_state_change(
            zeroconf: Zeroconf,
            service_type: str,
            name: str,
            state_change: ServiceStateChange,
        ) -> None:
            if state_change is ServiceStateChange.Added:
                asyncio.ensure_future(self.add_service(zeroconf, service_type, name))
            else:
                return

        return async_on_service_state_change

    def get_found_devices(self) -> list[HueBridgeDiscoverInfo]:
        """Returns all the found devices"""
        return self._found_devices


async def discover_hue_bridges(mDNS_discovery: bool) -> list[HueBridgeDiscoverInfo]:
    """Discovers all Phillips Hue bridges that are available on the
    current network

    Args:
        mDNS_discovery (bool): Whether to use mDNS for discovery

    Raises:
        HueBridgesDiscoveryError: When not using mDNS but getting rate limited
    """
    if mDNS_discovery:
        zeroconf = AsyncZeroconf()
        listener = HueDiscoveryListener()
        browser = AsyncServiceBrowser(
            zeroconf.zeroconf,
            "_hue._tcp.local.",
            handlers=[listener.get_service_handler()],
        )
        # Wait 5 seconds to collect as many as possible
        await asyncio.sleep(5)

        await browser.async_cancel()
        await zeroconf.async_close()

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

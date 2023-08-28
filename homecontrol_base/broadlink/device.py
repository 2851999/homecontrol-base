from typing import Optional
from homecontrol_base.broadlink.structs import BroadlinkDeviceDiscoverInfo
from homecontrol_base.database.homecontrol_base import models
import broadlink

from homecontrol_base.exceptions import DeviceNotFoundError


class BroadlinkDevice:
    """Class for handling a Broadlink device"""

    _device_info: models.BroadlinkDeviceInfo
    _device: broadlink.Device

    def __init__(self, device_info: models.BroadlinkDeviceInfo):
        """Initialises and authenticates the device

        Args:
            device_info (models.BroadlinkDeviceInfo): Device info
        """

        self._device_info = device_info

        # Connect to the device
        self._device = broadlink.hello(device_info.ip_address)
        self._device.auth()

    @staticmethod
    def _get_discover_info(device: broadlink.Device) -> BroadlinkDeviceDiscoverInfo:
        return BroadlinkDeviceDiscoverInfo(ip_address=device.host[0])

    @staticmethod
    def discover(ip_address: str) -> BroadlinkDeviceDiscoverInfo:
        """Attempts to discover a a specific Broadlink device

        Args:
            ip_address (str): IP address of the device

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        try:
            return BroadlinkDevice._get_discover_info(broadlink.hello(ip_address))
        except broadlink.e.NetworkTimeoutError:
            raise DeviceNotFoundError(
                f"Unable to find the Broadlink device with ip '{ip_address}'"
            )

    @staticmethod
    def discover_all() -> list[BroadlinkDeviceDiscoverInfo]:
        """Attempts ot discover all Broadlink devices available on the current
        network"""
        devices = broadlink.discover()

        # Parse and return
        return [BroadlinkDevice._get_discover_info(device) for device in devices]

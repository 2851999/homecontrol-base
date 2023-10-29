import time

import broadlink

from homecontrol_base.broadlink.exceptions import IncompatibleDeviceError, RecordTimeout
from homecontrol_base.broadlink.structs import BroadlinkDeviceDiscoverInfo
from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.exceptions import DeviceNotFoundError


class BroadlinkDevice:
    """Class for handling a Broadlink device"""

    # Max time we expect learning an IR packet to take (seconds)
    LEARNING_TIMEOUT = 10

    # Minimum time between querying if anything has been learnt yet (seconds)
    LEARNING_SLEEP_TIME = 1

    _device_info: models.BroadlinkDeviceInDB
    _device: broadlink.Device

    def __init__(self, device_info: models.BroadlinkDeviceInDB):
        """Initialises and authenticates the device

        Args:
            device_info (models.BroadlinkDeviceInDB): Device info
        """

        self._device_info = device_info

        # Connect to the device
        self._device = broadlink.hello(device_info.ip_address)
        self._device.auth()

    def record_ir_packet(self) -> bytes:
        """Puts the device into learning mode and waits until an IR packet is
        returned or a maximum timeout is reached

        Returns:
            bytes: The IR packet

        Raises:
            IncompatibleDeviceError: If the device is incompatible
            RecordTimeout: If the record times out
        """
        if not isinstance(self._device, broadlink.device.rmmini):
            raise IncompatibleDeviceError(
                "Incompatible device for recording IR packets"
            )
        # Start learning mode
        self._device.enter_learning()

        # Current packet
        packet = None

        # Start, elapsed and last tme we checked for an IR packet
        start_time = time.time()
        current_elapsed_time = 0

        # Keep checking for packets until we reach the timeout
        while current_elapsed_time < BroadlinkDevice.LEARNING_TIMEOUT:
            # Wait
            time.sleep(BroadlinkDevice.LEARNING_SLEEP_TIME)
            current_elapsed_time = time.time() - start_time

            # Check
            try:
                packet = self._device.check_data()
                return packet
            except broadlink.exceptions.ReadError:
                pass

        raise RecordTimeout("Failed to record an IR packet")

    def send_ir_packet(self, packet: bytes):
        """Sends an IR packet to the device

        Args:
            packet (bytes): Packet to send

        Raises:
            IncompatibleDeviceError: If the device is incompatible
        """
        if not isinstance(self._device, broadlink.device.rmmini):
            raise IncompatibleDeviceError("Incompatible device for sending IR packets")

        self._device.send_data(packet)

    @property
    def info(self) -> models.BroadlinkDeviceDiscoverInfo:
        """Returns information about the device"""
        return self._device_info

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

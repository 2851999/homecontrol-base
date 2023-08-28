from homecontrol_base.broadlink.device import BroadlinkDevice
from homecontrol_base.broadlink.structs import BroadlinkDeviceDiscoverInfo
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)
from homecontrol_base.database.homecontrol_base import models


class BroadlinkManager:
    """Manages a set of Broadlink devices"""

    _devices: dict[str, BroadlinkDevice]

    def __init__(self):
        self._devices = {}

        self._load_all()

    def _load_device(self, device_info: models.BroadlinkDeviceInfo) -> BroadlinkDevice:
        """Adds a device into _devices"""
        device = BroadlinkDevice(device_info)
        self._devices[device_info.id] = device
        return device

    def _load_all(self):
        with homecontrol_db.connect() as conn:
            devices = conn.get_broadlink_devices()
            for device_info in devices:
                self._load_device(device_info)

    def get_device(self, device_id: str) -> BroadlinkDevice:
        """Returns a Broadlink device given its id

        Attempts to load from database if not already loaded

        Args:
            device_id (str): ID of the device to get

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        device = self._devices.get(device_id)

        if not device:
            # Attempt to load it
            with homecontrol_db.connect() as conn:
                device = self._load_device(conn.get_broadlink_device(device_id))
        return device

    def get_device_by_name(self, device_name: str) -> BroadlinkDevice:
        """Returns a device given its name - slower than get_device

        Attempts to load from the database if not already loaded

        Args:
            device_name (str): The name of the device to get

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        # Look up the device in the database (so can get id)
        with homecontrol_db.connect() as conn:
            device_info = conn.get_broadlink_device_by_name(device_name)
        device = self._devices.get(device_info.id)
        if not device:
            device = self._load_device(device_info)
        return device

    def add_device(self, name: str, ip_address: str) -> BroadlinkDevice:
        """Adds a Broadlink device

        Args:
            name (str): Name to label the device
            ip_address (str): IP address of the device to add

        Raises:
            DeviceNotFoundError: If unable to find the device
        """
        discover_info = BroadlinkDevice.discover(ip_address=ip_address)
        device_info = models.BroadlinkDeviceInfo(
            name=name, ip_address=discover_info.ip_address
        )
        with homecontrol_db.connect() as conn:
            device_info = conn.create_broadlink_device(device_info)
        return self._load_device(device_info)

    def record_action(self, device_id: str, name: str) -> models.BroadlinkAction:
        """Records an action from a Broadlink device and saves it to the
        database

        Args:
            device_id (str): ID of the device to record the action on
            name (str): Name to label the action

        Raises:
            DeviceNotFoundError: If the device isn't found
            IncompatibleDeviceError: If the device is incompatible
            RecordTimeout: If the record times out
        """
        # Obtain from device
        packet = self.get_device(device_id).record_ir_packet()

        # Save to database
        action = models.BroadlinkAction(name=name, packet=packet)
        with homecontrol_db.connect() as conn:
            action = conn.create_broadlink_action(action)
        return action

    def play_action(self, device_id: str, action_id: str):
        """Plays an action on a Broadlink device

        Args:
            device_id (str): ID of the device to playback the action on
            action_id (str): ID of the action to playback

        Raises:
            DeviceNotFoundError: If the device isn't found
            IncompatibleDeviceError: If the device is incompatible
            ActionNotFoundError: If the action isn't found
        """
        # Obtain the action
        with homecontrol_db.connect() as conn:
            action = conn.get_broadlink_action(action_id)
        # Playback
        self.get_device(device_id).send_ir_packet(action.packet)

from homecontrol_base.aircon.device import ACDevice
from homecontrol_base.config.midea import MideaConfig
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)
from homecontrol_base.database.homecontrol_base.models import ACDeviceInfo
from homecontrol_base.exceptions import DeviceNotFoundError


class ACManager:
    """Manages a set of ACDevice instances"""

    _lazy_load: bool
    _loaded_all: bool

    _midea_config: MideaConfig
    _devices: dict[str, ACDevice]

    def __init__(self, lazy_load: bool = True):
        """Constructor

        Args:
            lazy_load (bool): Whether to load devices only when they are
                              needed. When True will only load all available
                              devices immediately
        """
        self._lazy_load = lazy_load
        self._loaded_all = False
        self._midea_config = MideaConfig()
        self._devices = {}

        # Load all devices if requested
        if not lazy_load:
            self._load_all()

    def _load_device(self, device_info: ACDeviceInfo) -> ACDevice:
        """Adds a device into _devices"""
        device = ACDevice(device_info)
        self._devices[device_info.id] = device
        return device

    def _load_all(self):
        with homecontrol_db.connect() as conn:
            devices = conn.get_ac_devices()
            for device_info in devices:
                self._load_device(device_info)
        self._loaded_all = True

    def get_device(self, device_id: str) -> ACDevice:
        """Returns a device given it's id

        Attempts to load from the database if not already loaded

        Args:
            device_id (str): The ID of the device to get

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        device = self._devices.get(device_id)
        if not device:
            # Attempt to load it
            with homecontrol_db.connect() as conn:
                device = self._load_device(conn.get_ac_device(device_id))
        return device

    def get_device_by_name(self, device_name: str) -> ACDevice:
        """Returns a device given it's name - slower than get_device

        Attempts to load from the database if not already loaded

        Args:
            device_name (str): The name of the device to get

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        # Look up the device in the database (so can get id)
        with homecontrol_db.connect() as conn:
            device_info = conn.get_ac_device_by_name(device_name)
        device = self._devices.get(device_info.id)
        if not device:
            device = self._load_device(device_info)
        return device

    def add_device(self, name: str, ip_address: str) -> ACDevice:
        """Adds an air conditioning device

        Args:
            name (str): Name to describe the device
            ip_address (str): IP address of the device

        Returns:
            str: The new device's id

        Raises:
            DeviceConnectionError: When an error occurs while attempting to
                                   connect to the device
            DeviceNotFoundError: When the device isn't found
        """
        device_info = ACDevice.discover(
            name=name, ip_address=ip_address, account=self._midea_config.account
        )
        with homecontrol_db.connect() as conn:
            device_info = conn.create_ac_device(device_info)
        return self._load_device(device_info)

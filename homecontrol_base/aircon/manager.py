from homecontrol_base.aircon.device import ACDevice
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)
from homecontrol_base.database.homecontrol_base.models import ACDeviceInfo
from homecontrol_base.exceptions import DeviceNotFoundError


class ACManager:
    """Manages a set of ACDevice instances"""

    _lazy_load: bool
    _loaded_all: bool

    _devices: dict[str, ACDevice]

    def __init__(self, lazy_load: bool = False):
        """Constructor

        Args:
            lazy_load (bool): Whether to load devices only when they are
                              needed. When True will only load all available
                              devices immediately
        """
        self._lazy_load = lazy_load
        self._loaded_all = False
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

            if not device:
                raise DeviceNotFoundError(
                    f"Air conditioning unit with id '{device_id}' was not found"
                )
        return device

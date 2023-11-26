from homecontrol_base.broadlink.device import BroadlinkDevice
from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.database.homecontrol_base.database import (
    HomeControlBaseDatabaseConnection,
)
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_base_db,
)


class BroadlinkManager:
    """Manages a set of Broadlink devices"""

    _devices: dict[str, BroadlinkDevice]

    def __init__(self):
        self._devices = {}

        self._load_all()

    def _load_device(self, device_info: models.BroadlinkDeviceInDB) -> BroadlinkDevice:
        """Adds a device into _devices"""
        device = BroadlinkDevice(device_info)
        self._devices[device_info.id] = device
        return device

    def _load_all(self):
        with homecontrol_base_db.connect() as conn:
            devices = conn.broadlink_devices.get_all()
            for device_info in devices:
                self._load_device(device_info)

    def get_device(
        self, db_conn: HomeControlBaseDatabaseConnection, device_id: str
    ) -> BroadlinkDevice:
        """Returns a Broadlink device given its id

        Attempts to load from database if not already loaded

        Args:
            db_conn (HomeControlBaseDatabaseConnection): Database connection
                    to use in the event a device needs to be looked up
            device_id (str): ID of the device to get

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        device = self._devices.get(device_id)

        if not device:
            # Attempt to load it
            device = self._load_device(db_conn.broadlink_devices.get(device_id))
        return device

    def add_device(self, device_info: models.BroadlinkDeviceInDB) -> BroadlinkDevice:
        """Adds a Broadlink device

        Args:
            device_info (BroadlinkDeviceInDB): Device info

        Returns:
            BroadlinkDevice: The new device

        Raises:
            DeviceNotFoundError: If unable to find the device
        """
        return self._load_device(device_info)

    def remove_device(self, device_id: str) -> None:
        """Removes the device with the given ID

        Args:
            device_id (str): ID of the device to delete

        Raises:
            DeviceNotFoundError: When the device isn't found
        """
        # Delete from the database
        with homecontrol_base_db.connect() as conn:
            conn.broadlink_devices.delete(device_id)
        # Remove from manager if already loaded
        if device_id in self._devices:
            del self._devices[device_id]

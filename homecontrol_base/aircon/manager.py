from homecontrol_base.aircon.device import ACDevice
from homecontrol_base.config.midea import MideaConfig
from homecontrol_base.database.homecontrol_base.database import (
    HomeControlBaseDatabaseConnection,
)
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_base_db,
)
from homecontrol_base.database.homecontrol_base.models import ACDeviceInfoInDB


class ACManager:
    """Manages a set of ACDevice instances"""

    _midea_config: MideaConfig
    _devices: dict[str, ACDevice]

    def __init__(self, lazy_load: bool = True):
        """Constructor"""
        self._lazy_load = lazy_load
        self._midea_config = MideaConfig()
        self._devices = {}

    async def initialise_all_devices(self):
        """Initialises and authenticates all devices

        Should only be called if don't want to lazy_load the devices
        and instead want fast access to all of the devices at the cost
        of waiting for this function to finish.

        Should be called immediately after __init__
        """

        # Load all devices
        await self._load_all()

    async def _load_device(self, device_info: ACDeviceInfoInDB) -> ACDevice:
        """Adds a device into _devices

        Raises:
            ACAuthenticationError: If authentication fails for the device
        """
        device = ACDevice(device_info)
        await device.initialise()
        # Must convert to string here as device_info.id is a UUID from the database
        self._devices[str(device_info.id)] = device
        return device

    async def _load_all(self):
        """Loads all devices from the database

        Raises:
            ACAuthenticationError: If authentication fails for any devices
        """
        with homecontrol_base_db.connect() as conn:
            devices = conn.ac_devices.get_all()
            for device_info in devices:
                await self._load_device(device_info)

    async def get_device(
        self, db_conn: HomeControlBaseDatabaseConnection, device_id: str
    ) -> ACDevice:
        """Returns a device given its id

        Attempts to load from the database if not already loaded

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
            device = await self._load_device(db_conn.ac_devices.get(device_id))
        return device

    async def add_device(self, device_info: ACDeviceInfoInDB) -> ACDevice:
        """Adds an air conditioning device

        Args:
            device_info (ACDeviceInfoInDB): Device info

        Returns:
            ACDevice: The new device

        Raises:
            DeviceConnectionError: When an error occurs while attempting to
                                   connect to the device
            DeviceNotFoundError: When the device isn't found
        """
        return await self._load_device(device_info)

    def remove_device(self, device_id: str) -> None:
        """Removes the device with the given ID (including from the database)

        Args:
            device_id (str): ID of the device to remove

        Raises:
            DeviceNotFoundError: When the device isn't found
        """
        # Delete from the database
        with homecontrol_base_db.connect() as conn:
            conn.ac_devices.delete(device_id)
        # Remove from manager if already loaded
        if device_id in self._devices:
            del self._devices[device_id]

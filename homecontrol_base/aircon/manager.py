from homecontrol_base.aircon.device import ACDevice
from homecontrol_base.config.midea import MideaConfig
from homecontrol_base.database.homecontrol_base.database import (
    HomeControlBaseDatabaseConnection,
)
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)
from homecontrol_base.database.homecontrol_base.models import ACDeviceInfoInDB


class ACManager:
    """Manages a set of ACDevice instances"""

    _lazy_load: bool

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
        self._midea_config = MideaConfig()
        self._devices = {}

        # Load all devices if requested
        if not lazy_load:
            self._load_all()

    def _load_device(self, device_info: ACDeviceInfoInDB) -> ACDevice:
        """Adds a device into _devices"""
        device = ACDevice(device_info)
        self._devices[device_info.id] = device
        return device

    def _load_all(self):
        """Loads all devices from the database"""
        with homecontrol_db.connect() as conn:
            devices = conn.ac_devices.get_all()
            for device_info in devices:
                self._load_device(device_info)

    def get_device(
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
            device = self._load_device(db_conn.ac_devices.get(device_id))
        return device

    def add_device(self, device_info: ACDeviceInfoInDB) -> ACDevice:
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
        return self._load_device(device_info)

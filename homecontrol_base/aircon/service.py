from homecontrol_base.aircon.device import ACDevice
from homecontrol_base.aircon.manager import ACManager
from homecontrol_base.database.homecontrol_base.database import (
    HomeControlBaseDatabaseConnection,
)
from homecontrol_base.service.core import BaseService


class ACService(BaseService[HomeControlBaseDatabaseConnection]):
    """Service for handling AC devices"""

    _ac_manager: ACManager

    def __init__(
        self,
        db_conn: HomeControlBaseDatabaseConnection,
        ac_manager: ACManager,
    ):
        super().__init__(db_conn)

        self._ac_manager = ac_manager

    async def get_device(self, device_id: str) -> ACDevice:
        """Returns a device given its id

        Attempts to load from the database if not already loaded

        Args:
            device_id (str): ID of the device to get

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        return await self._ac_manager.get_device(
            db_conn=self._db_conn, device_id=device_id
        )

    async def get_device_by_name(self, device_name: str) -> ACDevice:
        """Returns a device given its name - slower than get_device

        Attempts to load from the database if not already loaded

        Args:
            device_name (str): The name of the device to get

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        # Look up the device in the database (so can get id)
        device_info = self._db_conn.ac_devices.get_by_name(device_name)
        return await self._ac_manager.get_device(
            db_conn=self._db_conn, device_id=str(device_info.id)
        )

    async def add_device(self, name: str, ip_address: str) -> ACDevice:
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
        device_info = await ACDevice.discover(
            name=name,
            ip_address=ip_address,
            account=self._ac_manager._midea_config.account,
        )
        device_info = self._db_conn.ac_devices.create(device_info)
        return await self._ac_manager.add_device(device_info=device_info)

    def remove_device(self, device_id: str) -> None:
        """Removes an air conditioning device

        Args:
            device_id (str): ID of the device to remove

        Raises:
            DeviceNotFoundError: When the device isn't found
        """
        self._ac_manager.remove_device(device_id)

from homecontrol_base.broadlink.device import BroadlinkDevice
from homecontrol_base.broadlink.manager import BroadlinkManager
from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.database.homecontrol_base.database import (
    HomeControlBaseDatabaseConnection,
)
from homecontrol_base.service.core import BaseService


class BroadlinkService(BaseService[HomeControlBaseDatabaseConnection]):
    """Service for handling Broadlink devices"""

    _broadlink_manager: BroadlinkManager

    def __init__(
        self,
        db_conn: HomeControlBaseDatabaseConnection,
        broadlink_manager: BroadlinkManager,
    ):
        super().__init__(db_conn)

        self._broadlink_manager = broadlink_manager

    def get_device(self, device_id: str) -> BroadlinkDevice:
        """Returns a Broadlink device given its id

        Attempts to load from database if not already loaded

        Args:
            device_id (str): ID of the device to get

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        return self._broadlink_manager.get_device(
            db_conn=self._db_conn, device_id=device_id
        )

    def get_device_by_name(self, device_name: str) -> BroadlinkDevice:
        """Returns a device given its name - slower than get_device

        Attempts to load from the database if not already loaded

        Args:
            device_name (str): The name of the device to get

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        # Look up the device in the database (so can get id)
        device_info = self._db_conn.broadlink_devices.get_by_name(device_name)
        return self._broadlink_manager.get_device(
            db_conn=self._db_conn, device_id=str(device_info.id)
        )

    def add_device(self, name: str, ip_address: str) -> BroadlinkDevice:
        """Adds a Broadlink device

        Args:
            name (str): Name to label the device
            ip_address (str): IP address of the device to add

        Raises:
            DeviceNotFoundError: If unable to find the device
        """
        discover_info = BroadlinkDevice.discover(ip_address=ip_address)
        device_info = models.BroadlinkDeviceInDB(
            name=name, ip_address=discover_info.ip_address
        )
        device_info = self._db_conn.broadlink_devices.create(device_info)
        return self._broadlink_manager.add_device(device_info=device_info)

    def record_action(self, device_id: str, name: str) -> models.BroadlinkActionInDB:
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
        action = models.BroadlinkActionInDB(name=name, packet=packet)
        action = self._db_conn.broadlink_actions.create(action)
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
        action = self._db_conn.broadlink_actions.get(action_id)
        # Playback
        self.get_device(device_id).send_ir_packet(action.packet)

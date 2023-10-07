from uuid import UUID

from homecontrol_base import session
from homecontrol_base.database.core import DatabaseConnection
from homecontrol_base.database.homecontrol_base.models import BroadlinkDeviceInfo
from homecontrol_base.exceptions import DeviceNotFoundError


class BroadlinkDevicesDBConnection(DatabaseConnection):
    """Handles BroadlinkDeviceInfo's in the database"""

    def __init__(self, session: session):
        super().__init__(session)

    def create(self, device: BroadlinkDeviceInfo) -> BroadlinkDeviceInfo:
        """Adds a BroadlinkDeviceInfo to the database"""
        self._session.add(device)
        self._session.commit()
        self._session.refresh(device)
        return device

    def get(self, device_id: str) -> BroadlinkDeviceInfo:
        """Returns BroadlinkDeviceInfo given a device's id

        Args:
            device_id (str): The ID of the device

        Returns:
            BroadlinkDeviceInfo: Info about the device

        Raises:
            DeviceNotFoundError: If the device isn't found
        """

        device_info = (
            self._session.query(BroadlinkDeviceInfo)
            .filter(BroadlinkDeviceInfo.id == UUID(device_id))
            .first()
        )
        if not device_info:
            raise DeviceNotFoundError(
                f"Broadlink device with id '{device_id}' was not found"
            )
        return device_info

    def get_by_name(self, device_name: str) -> BroadlinkDeviceInfo:
        """Returns BroadlinkDeviceInfo given a device's name

        Args:
            device_name (str): The name of the Broadlink device

        Returns:
            BroadlinkDeviceInfo: Info about the device

        Raises:
            DeviceNotFoundError: If the device isn't found
        """

        device_info = (
            self._session.query(BroadlinkDeviceInfo)
            .filter(BroadlinkDeviceInfo.name == device_name)
            .first()
        )
        if not device_info:
            raise DeviceNotFoundError(
                f"Broadlink device with name '{device_name}' was not found"
            )
        return device_info

    def get_all(self) -> list[BroadlinkDeviceInfo]:
        """Returns a list of information about all Broadlink devices"""
        return self._session.query(BroadlinkDeviceInfo).all()

    def delete(self, device_id: str):
        """Deletes an BroadlinkDeviceInfo given the device's id

        Args:
            device_id (str): The ID of Broadlink device

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        rows_deleted = (
            self._session.query(BroadlinkDeviceInfo)
            .filter(BroadlinkDeviceInfo.id == UUID(device_id))
            .delete()
        )

        if rows_deleted == 0:
            raise DeviceNotFoundError(
                f"Broadlink device with id '{device_id}' was not found"
            )

        self._session.commit()

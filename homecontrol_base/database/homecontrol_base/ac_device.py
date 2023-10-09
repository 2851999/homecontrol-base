from uuid import UUID

from homecontrol_base import session
from homecontrol_base.database.core import DatabaseConnection
from homecontrol_base.database.homecontrol_base.models import ACDeviceInfoInDB
from homecontrol_base.exceptions import DeviceNotFoundError


class ACDevicesDBConnection(DatabaseConnection):
    """Handles ACDeviceInfoInDB's in the database"""

    def __init__(self, session: session):
        super().__init__(session)

    def create(self, device: ACDeviceInfoInDB) -> ACDeviceInfoInDB:
        """Adds an ACDeviceInfoInDB to the database"""
        self._session.add(device)
        self._session.commit()
        self._session.refresh(device)
        return device

    def get(self, device_id: str) -> ACDeviceInfoInDB:
        """Returns ACDeviceInfoInDB given an air conditioning unit's device id

        Args:
            device_id (str): The ID of the air conditioning unit

        Returns:
            ACDeviceInfoInDB: Info about the device

        Raises:
            DeviceNotFoundError: If the device isn't found
        """

        device_info = (
            self._session.query(ACDeviceInfoInDB)
            .filter(ACDeviceInfoInDB.id == UUID(device_id))
            .first()
        )
        if not device_info:
            raise DeviceNotFoundError(
                f"Air conditioning unit with id '{device_id}' was not found"
            )
        return device_info

    def get_by_name(self, device_name: str) -> ACDeviceInfoInDB:
        """Returns ACDeviceInfoInDB given an air conditioning unit's device id

        Args:
            device_name (str): The name of the air conditioning unit

        Returns:
            ACDeviceInfoInDB: Info about the device

        Raises:
            DeviceNotFoundError: If the device isn't found
        """

        device_info = (
            self._session.query(ACDeviceInfoInDB)
            .filter(ACDeviceInfoInDB.name == device_name)
            .first()
        )
        if not device_info:
            raise DeviceNotFoundError(
                f"Air conditioning unit with name '{device_name}' was not found"
            )
        return device_info

    def get_all(self) -> list[ACDeviceInfoInDB]:
        """Returns a list of information about all air conditioning devices"""
        return self._session.query(ACDeviceInfoInDB).all()

    def delete(self, device_id: str):
        """Deletes an ACDeviceInfoInDB given the air conditioning unit's device id

        Args:
            device_id (str): The ID of the air conditioning unit

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        rows_deleted = (
            self._session.query(ACDeviceInfoInDB)
            .filter(ACDeviceInfoInDB.id == UUID(device_id))
            .delete()
        )

        if rows_deleted == 0:
            raise DeviceNotFoundError(
                f"Air conditioning unit with id '{device_id}' was not found"
            )

        self._session.commit()

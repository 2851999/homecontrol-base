from uuid import UUID

from sqlalchemy.orm import Session

from homecontrol_base.config.database import DatabaseConfig
from homecontrol_base.database.core import Database, DatabaseConnection
from homecontrol_base.database.homecontrol_base.models import ACDeviceInfo, Base
from homecontrol_base.exceptions import DeviceNotFoundError


class HomecontrolBaseDatabaseConnection(DatabaseConnection):
    """Class for handling a connection to the homecontrol-base database"""

    def __init__(self, session: Session):
        super().__init__(session)

    """Below follows various methods for modifying the database"""

    """--------------------- Air conditioning devices ---------------------"""

    def create_ac_device(self, device: ACDeviceInfo) -> ACDeviceInfo:
        """Adds an ACDeviceInfo to the database"""
        self._session.add(device)
        self._session.commit()
        self._session.refresh(device)
        return device

    def get_ac_device(self, device_id: str) -> ACDeviceInfo:
        """Returns ACDevice info given an air conditioning unit's device ID

        Args:
            device_id (str): The ID of the air conditioning unit

        Returns:
            ACDeviceInfo: Info about the device

        Raises:
            DeviceNotFoundError: If the device isn't found
        """

        device_info = (
            self._session.query(ACDeviceInfo)
            .filter(ACDeviceInfo.id == UUID(device_id))
            .first()
        )
        if not device_info:
            raise DeviceNotFoundError(
                f"Air conditioning unit with id '{device_id}' was not found"
            )
        return device_info

    def get_ac_devices(self) -> list[ACDeviceInfo]:
        """Returns a list of information about all air conditioning devices"""
        return self._session.query(ACDeviceInfo).all()

    def delete_ac_device(self, device_id: str):
        """Deletes an ACDevice info given the air conditioning unit's device id

        Args:
            device_id (str): The ID of the air conditioning unit

        Raises:
            DeviceNotFoundError: If the device isn't found
        """
        rows_deleted = (
            self._session.query(ACDeviceInfo)
            .filter(ACDeviceInfo.id == UUID(device_id))
            .delete()
        )

        if rows_deleted == 0:
            raise DeviceNotFoundError(
                f"Air conditioning unit with id '{device_id}' was not found"
            )

        self._session.commit()


class HomecontrolBaseDatabase(Database[HomecontrolBaseDatabaseConnection]):
    """Database for storing information handled by homecontrol-base"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(
            "homecontrol_base", Base, HomecontrolBaseDatabaseConnection, config
        )


database = HomecontrolBaseDatabase(DatabaseConfig())

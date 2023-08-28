from uuid import UUID

from sqlalchemy.orm import Session

from homecontrol_base.config.database import DatabaseConfig
from homecontrol_base.database.core import Database, DatabaseConnection
from homecontrol_base.database.homecontrol_base.models import (
    ACDeviceInfo,
    Base,
    BroadlinkDeviceInfo,
    HueBridgeInfo,
)
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
        """Returns ACDeviceInfo given an air conditioning unit's device id

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

    def get_ac_device_by_name(self, device_name: str) -> ACDeviceInfo:
        """Returns ACDeviceInfo given an air conditioning unit's device id

        Args:
            device_name (str): The name of the air conditioning unit

        Returns:
            ACDeviceInfo: Info about the device

        Raises:
            DeviceNotFoundError: If the device isn't found
        """

        device_info = (
            self._session.query(ACDeviceInfo)
            .filter(ACDeviceInfo.name == device_name)
            .first()
        )
        if not device_info:
            raise DeviceNotFoundError(
                f"Air conditioning unit with name '{device_name}' was not found"
            )
        return device_info

    def get_ac_devices(self) -> list[ACDeviceInfo]:
        """Returns a list of information about all air conditioning devices"""
        return self._session.query(ACDeviceInfo).all()

    def delete_ac_device(self, device_id: str):
        """Deletes an ACDeviceInfo given the air conditioning unit's device id

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

    """-------------------------- Hue bridges  --------------------------"""

    def create_hue_bridge(self, bridge: HueBridgeInfo) -> HueBridgeInfo:
        """Adds an HueBridgeInfo to the database"""
        self._session.add(bridge)
        self._session.commit()
        self._session.refresh(bridge)
        return bridge

    def get_hue_bridge(self, bridge_id: str) -> HueBridgeInfo:
        """Returns HueBridgeInfo given an Hue bridge's id

        Args:
            bridge_id (str): The ID of the Hue bridge

        Returns:
            HueBridgeInfo: Info about the device

        Raises:
            DeviceNotFoundError: If the device isn't found
        """

        device_info = (
            self._session.query(HueBridgeInfo)
            .filter(HueBridgeInfo.id == UUID(bridge_id))
            .first()
        )
        if not device_info:
            raise DeviceNotFoundError(f"Hue bridge with id '{bridge_id}' was not found")
        return device_info

    def get_hue_bridge_by_name(self, bridge_name: str) -> HueBridgeInfo:
        """Returns HueBridgeInfo given a Hue bridge's name

        Args:
            bridge_name (str): The name of the Hue bridge

        Returns:
            HueBridgeInfo: Info about the device

        Raises:
            DeviceNotFoundError: If the device isn't found
        """

        device_info = (
            self._session.query(HueBridgeInfo)
            .filter(HueBridgeInfo.name == bridge_name)
            .first()
        )
        if not device_info:
            raise DeviceNotFoundError(
                f"Hue bridge with name '{bridge_name}' was not found"
            )
        return device_info

    def get_hue_bridges(self) -> list[HueBridgeInfo]:
        """Returns a list of information about all Hue bridges"""
        return self._session.query(HueBridgeInfo).all()

    def delete_hue_bridge(self, bridge_id: str):
        """Deletes an HueBridgeInfo given the Hue bridge's id

        Args:
            bridge_id (str): The ID of the Hue bridge

        Raises:
            DeviceNotFoundError: If the bridge isn't found
        """
        rows_deleted = (
            self._session.query(HueBridgeInfo)
            .filter(HueBridgeInfo.id == UUID(bridge_id))
            .delete()
        )

        if rows_deleted == 0:
            raise DeviceNotFoundError(f"Hue bridge with id '{bridge_id}' was not found")

        self._session.commit()

    """-------------------------- Broadlink devices  --------------------------"""

    def create_broadlink_device(
        self, device: BroadlinkDeviceInfo
    ) -> BroadlinkDeviceInfo:
        """Adds a BroadlinkDeviceInfo to the database"""
        self._session.add(device)
        self._session.commit()
        self._session.refresh(device)
        return device

    def get_broadlink_device(self, device_id: str) -> BroadlinkDeviceInfo:
        """Returns BroadlinkDeviceInfo given an Broadlink device's id

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

    def get_broadlink_device_by_name(self, device_name: str) -> BroadlinkDeviceInfo:
        """Returns BroadlinkDeviceInfo given a Broadlink device's name

        Args:
            bridge_name (str): The name of the Hue bridge

        Returns:
            HueBridgeInfo: Info about the device

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

    def get_broadlink_devices(self) -> list[BroadlinkDeviceInfo]:
        """Returns a list of information about all Broadlink devices"""
        return self._session.query(BroadlinkDeviceInfo).all()

    def delete_broadlink_device(self, device_id: str):
        """Deletes an BroadlinkDeviceInfo given the Broadlink device's id

        Args:
            device_id (str): The ID of the Hue bridge

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


class HomecontrolBaseDatabase(Database[HomecontrolBaseDatabaseConnection]):
    """Database for storing information handled by homecontrol-base"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(
            "homecontrol_base", Base, HomecontrolBaseDatabaseConnection, config
        )


database = HomecontrolBaseDatabase(DatabaseConfig())

from uuid import UUID

from homecontrol_base import session
from homecontrol_base.database.core import DatabaseConnection
from homecontrol_base.database.homecontrol_base.models import HueBridgeInfo
from homecontrol_base.exceptions import DeviceNotFoundError


class HueBridgesDBConnection(DatabaseConnection):
    """Handles HueBridgeInfo's in the database"""

    def __init__(self, session: session):
        super().__init__(session)

    def create(self, bridge: HueBridgeInfo) -> HueBridgeInfo:
        """Adds an HueBridgeInfo to the database"""
        self._session.add(bridge)
        self._session.commit()
        self._session.refresh(bridge)
        return bridge

    def get(self, bridge_id: str) -> HueBridgeInfo:
        """Returns HueBridgeInfo given an bridge's id

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

    def get_by_name(self, bridge_name: str) -> HueBridgeInfo:
        """Returns HueBridgeInfo given a bridge's name

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

    def get_all(self) -> list[HueBridgeInfo]:
        """Returns a list of information about all Hue bridges"""
        return self._session.query(HueBridgeInfo).all()

    def delete(self, bridge_id: str):
        """Deletes an HueBridgeInfo given the bridge's id

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

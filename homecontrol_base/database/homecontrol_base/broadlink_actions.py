from uuid import UUID

from homecontrol_base import session
from homecontrol_base.broadlink.exceptions import ActionNotFoundError
from homecontrol_base.database.core import DatabaseConnection
from homecontrol_base.database.homecontrol_base.models import BroadlinkActionInDB


class BroadlinkActionsDBConnection(DatabaseConnection):
    """Handles BroadlinkActionInDB's in the database"""

    def __init__(self, session: session):
        super().__init__(session)

    def create(self, action: BroadlinkActionInDB) -> BroadlinkActionInDB:
        """Adds a BroadlinkActionInDB to the database"""
        self._session.add(action)
        self._session.commit()
        self._session.refresh(action)
        return action

    def get(self, action_id: str) -> BroadlinkActionInDB:
        """Returns BroadlinkActionInDB given an action's id

        Args:
            action_id (str): The ID of the action

        Returns:
            BroadlinkActionInDB: Info about the action

        Raises:
            ActionNotFoundError: If the action isn't found
        """

        device_info = (
            self._session.query(BroadlinkActionInDB)
            .filter(BroadlinkActionInDB.id == UUID(action_id))
            .first()
        )
        if not device_info:
            raise ActionNotFoundError(
                f"Broadlink action with id '{action_id}' was not found"
            )
        return device_info

    def get_by_name(self, action_name: str) -> BroadlinkActionInDB:
        """Returns BroadlinkActionInDB given the actions name

        Args:
            action_name (str): The name of the Hue bridge

        Returns:
            BroadlinkActionInDB: Info about the action

        Raises:
            ActionNotFoundError: If the action isn't found
        """

        device_info = (
            self._session.query(BroadlinkActionInDB)
            .filter(BroadlinkActionInDB.name == action_name)
            .first()
        )
        if not device_info:
            raise ActionNotFoundError(
                f"Broadlink action with name '{action_name}' was not found"
            )
        return device_info

    def get_all(self) -> list[BroadlinkActionInDB]:
        """Returns a list of information about all Broadlink actions"""
        return self._session.query(BroadlinkActionInDB).all()

    def delete(self, action_id: str):
        """Deletes an BroadlinkActionInDB given the actions's id

        Args:
            action_id (str): The ID of the Broadlink action

        Raises:
            ActionNotFoundError: If the action isn't found
        """
        rows_deleted = (
            self._session.query(BroadlinkActionInDB)
            .filter(BroadlinkActionInDB.id == UUID(action_id))
            .delete()
        )

        if rows_deleted == 0:
            raise ActionNotFoundError(
                f"Broadlink action with id '{action_id}' was not found"
            )

        self._session.commit()

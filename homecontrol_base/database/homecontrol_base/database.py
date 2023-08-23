from uuid import UUID

from sqlalchemy.orm import Session

from homecontrol_base.config.database import DatabaseConfig
from homecontrol_base.database.core import Database, DatabaseConnection
from homecontrol_base.database.homecontrol_base.models import ACDeviceInfo, Base


class HomecontrolBaseDatabaseConnection(DatabaseConnection):
    """Class for handling a connection to the homecontrol-base database"""

    def __init__(self, session: Session):
        super().__init__(session)

    """Below follows various methods for modifying the database"""

    """--------------------- Air conditioning devices ---------------------"""

    def create_ac_device(self, device: ACDeviceInfo) -> ACDeviceInfo:
        self._session.add(device)
        self._session.commit()
        self._session.refresh(device)
        return device

    def get_ac_device(self, device_id: str) -> ACDeviceInfo:
        return (
            self._session.query(ACDeviceInfo)
            .filter(ACDeviceInfo.id == UUID(device_id))
            .first()
        )

    def get_ac_devices(self) -> list[ACDeviceInfo]:
        return self._session.query(ACDeviceInfo).all()

    def delete_ac_device(self, device_id: str):
        self._session.query(ACDeviceInfo).filter(
            ACDeviceInfo.id == UUID(device_id)
        ).delete()
        self._session.commit()


class HomecontrolBaseDatabase(Database[HomecontrolBaseDatabaseConnection]):
    """Database for storing information handled by homecontrol-base"""

    def __init__(self, config: DatabaseConfig) -> None:
        super().__init__(
            "homecontrol_base", Base, HomecontrolBaseDatabaseConnection, config
        )


database = HomecontrolBaseDatabase(DatabaseConfig())

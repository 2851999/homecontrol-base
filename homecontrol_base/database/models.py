import uuid

from sqlalchemy import UUID, Column, Integer, String

from homecontrol_base.database.base import Base


class ACDevice(Base):
    __tablename__ = "ac_devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    ip_address = Column(String)
    identifier = Column(Integer)
    key = Column(String)
    token = Column(String)

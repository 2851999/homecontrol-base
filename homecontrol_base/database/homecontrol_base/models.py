import uuid

from sqlalchemy import Column, Integer, String, Uuid

from homecontrol_base.database.homecontrol_base.database import Base


class ACDevice(Base):
    __tablename__ = "ac_devices"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    ip_address = Column(String)
    identifier = Column(Integer)
    key = Column(String)
    token = Column(String)

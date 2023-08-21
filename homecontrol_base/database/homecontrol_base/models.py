import uuid

from sqlalchemy import Column, Integer, String, Uuid
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ACDevice(Base):
    __tablename__ = "ac_devices"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    ip_address = Column(String)
    identifier = Column(Integer)
    key = Column(String)
    token = Column(String)

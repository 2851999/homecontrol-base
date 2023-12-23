import uuid

from sqlalchemy import Column, Integer, LargeBinary, String, Uuid
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ACDeviceInfoInDB(Base):
    __tablename__ = "ac_devices"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    ip_address = Column(String, unique=True)
    identifier = Column(Integer)
    key = Column(String)
    token = Column(String)


class HueBridgeInDB(Base):
    __tablename__ = "hue_bridges"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    ip_address = Column(String, unique=True)
    port = Column(Integer)
    identifier = Column(String)
    username = Column(String)
    client_key = Column(String)


class BroadlinkDeviceInDB(Base):
    __tablename__ = "broadlink_devices"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    ip_address = Column(String, unique=True)


class BroadlinkActionInDB(Base):
    __tablename__ = "broadlink_actions"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    packet = Column(LargeBinary)

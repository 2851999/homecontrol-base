from typing import Union
from pydantic import UUID4, BaseModel, field_validator
from pydantic.dataclasses import dataclass
from sqlalchemy import Uuid, create_engine

from homecontrol_base.aircon.device import ACDevice
from homecontrol_base.aircon.manager import ACManager
from homecontrol_base.config.database import DatabaseConfig
from homecontrol_base.config.hue import HueConfig
from homecontrol_base.config.midea import MideaConfig
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)
from homecontrol_base.hue.bridge import HueBridge
from homecontrol_base.hue.exceptions import HueBridgeButtonNotPressedError

#  config = MideaConfig()
# # config.account.username = "new_test"
# # config.save()

# print(config.account)

# device = ACDevice.discover("Test", "192.168.1.85", config.account)

# engine = create_engine("sqlite:///:memory:", echo=True)
# Base.metadata.create_all(engine)


homecontrol_db.create_tables()
# with homecontrol_db.connect() as session:
#     # print(session.create_ac_device(device))
#     # session.delete_ac_device("6927f184-ba42-4ae9-b4f1-c4c975a2966b")
#     # print([device.id for device in session.get_ac_devices()])

#     device = ACDevice(session.get_ac_device("873b9d88-aaac-4806-9f0a-2a1e9b85f498"))
#     state = device.get_state()
#     print(state)

ac_manager = ACManager()
# ac_manager.add_device("Test", "192.168.1.85")


# class Test(BaseModel):
#     id: str
#     name: str

#     class Config:
#         from_attributes = True

#     _extract_id = field_validator("id", mode="before")(lambda value: str(value))


# test = Test.model_validate(ac_manager.get_device_by_name("Test").get_info())
# print(test.model_dump())


# device = ac_manager.get_device("05e06c5f-a3db-4397-843a-e479e6a2a310")
# print(device.get_state())

hue_config = HueConfig()
bridges = HueBridge.discover()
auth_info = None
while not auth_info:
    try:
        HueBridge.authenticate("Home", bridges[0], hue_config.ca_cert)
    except HueBridgeButtonNotPressedError as err:
        input("Press enter once you have pressed the button on the Hue bridge")

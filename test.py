from pydantic import BaseModel
from sqlalchemy import create_engine

from homecontrol_base.aircon.device import ACDevice
from homecontrol_base.config.database import DatabaseConfig
from homecontrol_base.config.midea import MideaConfig
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)

#  config = MideaConfig()
# # config.account.username = "new_test"
# # config.save()

# print(config.account)

# device = ACDevice.discover("Test", "192.168.1.85", config.account)

# engine = create_engine("sqlite:///:memory:", echo=True)
# Base.metadata.create_all(engine)


homecontrol_db.create_tables()
with homecontrol_db.connect() as session:
    # print(session.create_ac_device(device))
    # session.delete_ac_device("6927f184-ba42-4ae9-b4f1-c4c975a2966b")
    # print([device.id for device in session.get_ac_devices()])

    device = ACDevice(session.get_ac_device("873b9d88-aaac-4806-9f0a-2a1e9b85f498"))
    state = device.get_state()
    print(state)

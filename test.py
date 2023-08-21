from sqlalchemy import create_engine

from homecontrol_base.aircon.device import ACDevice
from homecontrol_base.config.database import DatabaseConfig
from homecontrol_base.config.midea import MideaConfig
from homecontrol_base.database.homecontrol_base.database import db as homecontrol_db

# config = MideaConfig()
# # config.account.username = "new_test"
# # config.save()

# print(config.account)

# device = ACDevice.discover("Test", "192.168.1.85", config.account)
# print(device)

# engine = create_engine("sqlite:///:memory:", echo=True)
# Base.metadata.create_all(engine)

homecontrol_db.create_tables()
print(homecontrol_db.engine)
with homecontrol_db.connect() as session:
    print("HELLO")

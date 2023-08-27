from homecontrol_base.aircon.manager import ACManager
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)
from homecontrol_base.hue.manager import HueManager

# homecontrol_db.create_tables()


# def setup_ac():
#     ac_manager = ACManager()
#     ac_manager.add_device("Joel's Room", "192.168.1.77")
#     ac_manager.add_device("Games Room", "192.168.1.85")
#     ac_manager.add_device("Spare Room", "192.168.1.198")
#     ac_manager.add_device("Mum's Room", "192.168.1.237")


# def setup_hue():
#     hue_manager = HueManager()
#     hue_manager.discover_and_add_all_bridges()


# setup_ac()
# setup_hue()

hue_manager = HueManager()
bridge = hue_manager.get_bridge_by_name("Bridge0")

with bridge.connect_api() as conn:
    print(conn._session.get("/clip/v2/resource/light").json())

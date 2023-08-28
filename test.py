import json
from dataclasses import asdict
from typing import Optional

from pydantic import TypeAdapter, parse_obj_as
from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder

from homecontrol_base.aircon.manager import ACManager
from homecontrol_base.broadlink.manager import BroadlinkManager
from homecontrol_base.broadlink.structs import BroadlinkDeviceDiscoverInfo
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)
from homecontrol_base.hue.api.schema import (
    GroupedLightPut,
    LightGet,
    LightPut,
    RoomPost,
    ScenePost,
    ScenePut,
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


# def setup_broadlink():
#     broadlink_manager = BroadlinkManager()
#     broadlink_manager.add_device("Mum's Room", "192.168.1.126")


# setup_ac()
# setup_hue()
# setup_broadlink()

# hue_manager = HueManager()
# bridge = hue_manager.get_bridge_by_name("Bridge0")

# with bridge.connect_api() as conn:
#     # lights = conn.get_lights()
#     # for light in lights:
#     #     if light.on.on:
#     #         print(light.id)

#     # light = conn.get_light("19954fc6-4d4a-46df-ba9f-da730bfa9f9f")
#     # print(light)
#     # conn.put_light(
#     #     "19954fc6-4d4a-46df-ba9f-da730bfa9f9f", LightPut(**{"on": {"on": False}})
#     # )

#     # print(conn.get_scenes())
#     # print(conn.get_scene("b711b49f-0bb7-4a9a-b730-2bc6ca29c450"))
#     # conn.put_scene(
#     #     "b711b49f-0bb7-4a9a-b730-2bc6ca29c450",
#     #     ScenePut(**{"recall": {"action": "active"}}),
#     # )
#     # print(conn.get_rooms())
#     # print(conn.get_room("e7e6883f-85ae-4d28-8dab-7b783445acad"))
#     # print(conn.get_grouped_lights())
#     # print(conn.get_grouped_light("42e245c4-ef2a-447c-9b55-0f657862b0ac"))
#     # print(
#     #     conn.put_grouped_light(
#     #         "42e245c4-ef2a-447c-9b55-0f657862b0ac",
#     #         GroupedLightPut(**{"on": {"on": False}}),
#     #     )
#     # )

#     # print(
#     #     json.dumps(
#     #         conn._session.get("/clip/v2/resource/behavior_script").json(), indent=4
#     #     )
#     # )
#     # print(
#     #     json.dumps(
#     #         conn._session.get("/clip/v2/resource/behavior_instance").json(), indent=4
#     #     )
#     # )

#     # Need one action per light
#     # data = ScenePost(
#     #     **{
#     #         "actions": [
#     #             {
#     #                 "target": {
#     #                     "rid": "19954fc6-4d4a-46df-ba9f-da730bfa9f9f",
#     #                     "rtype": "light",
#     #                 },
#     #                 "action": {"on": {"on": True}},
#     #             },
#     #             {
#     #                 "target": {
#     #                     "rid": "9c76db66-26ad-43ee-b3b1-915be3060a4c",
#     #                     "rtype": "light",
#     #                 },
#     #                 "action": {
#     #                     "on": {"on": False},
#     #                 },
#     #             },
#     #         ],
#     #         "metadata": {"name": "Homecontrol"},
#     #         "group": {"rid": "e7e6883f-85ae-4d28-8dab-7b783445acad", "rtype": "room"},
#     #     }
#     # )
#     # print(conn.post_scene(data))
#     # print(conn.delete_scene("51e942ef-6fb4-4735-a1ac-efb1fd0b648f"))

#     # data = RoomPost(
#     #     **{"children": [], "metadata": {"name": "TestRoom", "archetype": "man_cave"}}
#     # )
#     # print(conn.post_room(data))
#     # print(conn.delete_room("5c61e8e8-bf18-471a-b393-b6f51fb2cbf3"))

broadlink_manager = BroadlinkManager()
device = broadlink_manager.get_device_by_name("Mum's Room")
print(device)

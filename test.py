import json
from dataclasses import asdict
from typing import Optional

from pydantic import TypeAdapter, parse_obj_as
from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder
from homecontrol_base.aircon.device import ACDevice

from homecontrol_base.aircon.manager import ACManager
from homecontrol_base.hue.discovery import discover_hue_bridges
from homecontrol_base.hue.structs import (
    HueRoomGroupedLightStateUpdate,
    HueRoomStateUpdate,
)
from homecontrol_base.utils import run_until_complete
from homecontrol_base.broadlink.manager import BroadlinkManager
from homecontrol_base.broadlink.structs import BroadlinkDeviceDiscoverInfo
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_base_db,
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
from homecontrol_base.service.homecontrol_base import create_homecontrol_base_service
from homecontrol_base.hue.bridge import HueBridge

# homecontrol_base_db.create_tables()


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
#     #         "metadata": {"name": "HomeControl"},
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

# broadlink_manager = BroadlinkManager()
# print(broadlink_manager.record_action("d8d759d1-0e53-4aee-b9d1-9d172cf3c08e", "Test1").id)
# broadlink_manager.play_action(
#     "d8d759d1-0e53-4aee-b9d1-9d172cf3c08e", "aa6aa93cfe0e450080b676a727f96f8e"
# )
# device = broadlink_manager.get_device("d8d759d1-0e53-4aee-b9d1-9d172cf3c08e")

with create_homecontrol_base_service() as service:
    bridge = service.hue.get_bridge_by_name("Home")

    with bridge.connect_api() as conn:
        lights = conn.get_lights()
#         for light in lights:
#             if light.on.on:
#                 print(light.id)

# with create_homecontrol_base_service() as service:
#     device = service.aircon.get_device_by_name("Games Room")
#     state = device.get_state()
#     print(state)
#     state.power = True
#     device.set_state(state)

# with create_homecontrol_base_service() as test:
#     print(test.broadlink.get_device("d8d759d1-0e53-4aee-b9d1-9d172cf3c08e"))


# async def setup_ac():
#     with create_homecontrol_base_service() as service:
#         await service.aircon.add_device("Joel's Room", "192.168.1.77")


#         await service.aircon.add_device("Games Room", "192.168.1.85")
#         await service.aircon.add_device("Spare Room", "192.168.1.198")
#         await service.aircon.add_device("Mum's Room", "192.168.1.237")


# run_until_complete(setup_ac)


# async def test_set_ac_state():
#     with create_homecontrol_base_service() as service:
#         device = await service.aircon.get_device_by_name("Games Room")
#         state = await device.get_state()
#         print(state)
#         state.power = False
#         await device.set_state(state)


# run_until_complete(test_set_ac_state)

# print(discover_hue_bridges(True))


# def print_json(dictionary):
#     print(json.dumps(dictionary, indent=2))


# class HueRoom:
#     name: str
#     grouped_light_id: str
#     lights: str


# with create_homecontrol_base_service() as service:
#     bridge = service.hue.get_bridge("1e9ffff0-960b-4dd9-8372-a16b6df69d0e")
#     # with bridge.connect_api() as conn:
#     #     for room in conn.get_rooms():
#     #         print_json(asdict(room))

#     #     print_json(
#     #         asdict(conn.get_grouped_light("42e245c4-ef2a-447c-9b55-0f657862b0ac"))
#     #     )

#     #     # for light in conn.get_lights():
#     #     #     print_json(asdict(light))

#     #     print_json(asdict(conn.get_device("e48696a0-c193-48c2-84c0-0d63a04a35d2")))
#     with bridge.connect() as conn:
#         print(conn.get_rooms())


# async def test():
#     with create_homecontrol_base_service() as service:
#         await service.aircon.get_device("d257751b-996a-4cc9-8009-a32bd38857dd")
#         await service.aircon.get_device("d257751b-996a-4cc9-8009-a32bd38857dd")
#         await service.aircon.get_device("d257751b-996a-4cc9-8009-a32bd38857dd")
#         print(len(service._ac_manager._devices))


# run_until_complete(test)

# with create_homecontrol_base_service() as service:
#     bridge = service.hue.get_bridge("1e9ffff0-960b-4dd9-8372-a16b6df69d0e")
#     with bridge.connect() as conn:
#         # print(conn.get_room("e7e6883f-85ae-4d28-8dab-7b783445acad"))
#         colour = list(
#             conn.get_room_state("e7e6883f-85ae-4d28-8dab-7b783445acad").lights.values()
#         )[1].colour
#         print(f"rgb({colour.r * 255}, {colour.g * 255}, {colour.b * 255})")

# print(conn.get_room_state("e7e6883f-85ae-4d28-8dab-7b783445acad"))
# print(
#     conn.set_room_state(
#         "e7e6883f-85ae-4d28-8dab-7b783445acad",
#         HueRoomStateUpdate(
#             grouped_light=HueRoomGroupedLightStateUpdate(on=False)
#         ),
#     )
# )
# print(
#     conn.set_room_state(
#         "e7e6883f-85ae-4d28-8dab-7b783445acad",
#         HueRoomStateUpdate(scene="7bd7f08f-2eac-4bcb-978c-bb49b13d5f5e"),
#     )
# )


# async def setup_ac():
#     # print(await HueBridge.discover(True))

#     with create_homecontrol_base_service() as service:
#         print(await service.hue.discover())


# run_until_complete(setup_ac)

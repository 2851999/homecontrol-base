import json
from dataclasses import asdict
from typing import Optional

from pydantic import TypeAdapter, parse_obj_as
from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder

from homecontrol_base.aircon.manager import ACManager
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)
from homecontrol_base.hue.api.schema import (
    GroupedLightPut,
    LightGet,
    LightPut,
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


# setup_ac()
# setup_hue()

hue_manager = HueManager()
bridge = hue_manager.get_bridge_by_name("Bridge0")

with bridge.connect_api() as conn:
    # lights = conn.get_lights()
    # for light in lights:
    #     if light.on.on:
    #         print(light.id)

    # light = conn.get_light("19954fc6-4d4a-46df-ba9f-da730bfa9f9f")
    # print(light)
    # conn.put_light(
    #     "19954fc6-4d4a-46df-ba9f-da730bfa9f9f", LightPut(**{"on": {"on": False}})
    # )

    # print(conn.get_scenes())
    # print(conn.get_scene("b711b49f-0bb7-4a9a-b730-2bc6ca29c450"))
    # conn.put_scene(
    #     "b711b49f-0bb7-4a9a-b730-2bc6ca29c450",
    #     ScenePut(**{"recall": {"action": "active"}}),
    # )
    # print(conn.get_rooms())
    # print(conn.get_room("e7e6883f-85ae-4d28-8dab-7b783445acad"))
    # print(conn.get_grouped_lights())
    # print(conn.get_grouped_light("42e245c4-ef2a-447c-9b55-0f657862b0ac"))
    # conn.put_grouped_light(
    #     "42e245c4-ef2a-447c-9b55-0f657862b0ac", GroupedLightPut(**{"on": {"on": False}})
    # )

    # print(
    #     json.dumps(
    #         conn._session.get("/clip/v2/resource/behavior_script").json(), indent=4
    #     )
    # )
    # print(
    #     json.dumps(
    #         conn._session.get("/clip/v2/resource/behavior_instance").json(), indent=4
    #     )
    # )


# @dataclass
# class Test:
#     test: str


# data = {"test": "hello", "another": "test"}
# print(Test(**data))


# @dataclass
# class Test2:
#     on: Optional[bool] = None


# @dataclass
# class Test3:
#     test1: Optional[str] = None
#     on: Optional[Test2] = None


# data = Test3()
# # data = Test3(**{"on": {"on": True}})
# data.test1 = "str"


# print(asdict(data, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
# print(json.dumps(data, default=pydantic_encoder))

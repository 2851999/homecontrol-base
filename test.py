from dataclasses import asdict
import json
from typing import Optional
from pydantic import TypeAdapter, parse_obj_as
from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder

from homecontrol_base.aircon.manager import ACManager
from homecontrol_base.database.homecontrol_base.database import (
    database as homecontrol_db,
)
from homecontrol_base.hue.api.schema import LightGet
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
    lights = conn.get_lights()
    print(len(lights))


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

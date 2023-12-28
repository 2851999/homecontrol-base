from enum import StrEnum
from typing import Optional

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from homecontrol_base.hue.api.colour import HueColour


@dataclass
class HueBridgeDiscoverInfo:
    """Stores info from the discovery of a Hue bridge"""

    id: str
    internalipaddress: str
    port: int


@dataclass
class HueRoomLight:
    """Stores basic info about a light found in a room"""

    name: str


@dataclass
class HueRoom:
    """Stores basic info about a room found via a bridge"""

    id: str
    name: str
    grouped_light_id: Optional[str]
    lights: dict[str, HueRoomLight]


@dataclass
class HueRoomGroupedLightState:
    on: Optional[bool] = None
    brightness: Optional[float] = None


@dataclass
class HueRoomLightState:
    """Stores info about the state of a specific light in a room"""

    name: str
    on: bool

    # Will be none for a plug
    brightness: Optional[float] = None
    colour_temperature: Optional[int] = None
    colour: Optional[HueColour] = None


class HueRoomSceneStatus(StrEnum):
    INACTIVE = "inactive"
    STATIC = "static"
    DYNAMIC_PALETTE = "dynamic_palette"


@dataclass
class HueRoomSceneState:
    """Stores basic info about the state of a scene found in a room"""

    name: str
    status: HueRoomSceneStatus


@dataclass
class HueRoomState:
    grouped_light: HueRoomGroupedLightState
    lights: dict[str, HueRoomLightState]
    scenes: dict[str, HueRoomSceneState]


class HueRoomGroupedLightStateUpdate(BaseModel):
    on: Optional[bool] = None
    brightness: Optional[float] = None


class HueRoomLightStateUpdate(BaseModel):
    on: Optional[bool] = None

    # Will be none for a plug
    brightness: Optional[float] = None
    colour_temperature: Optional[int] = None
    colour: Optional[HueColour] = None


class HueRoomStateUpdate(BaseModel):
    grouped_light: Optional[HueRoomGroupedLightStateUpdate] = None
    lights: Optional[dict[str, HueRoomLightStateUpdate]] = None

    # When specified will recall a scene given it's id (after any other updates)
    scene: Optional[str] = None

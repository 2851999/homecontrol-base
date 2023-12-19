from typing import Optional

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


@dataclass
class HueRoomState:
    grouped_light: HueRoomGroupedLightState
    lights: dict[str, HueRoomLightState]

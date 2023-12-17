from typing import Optional
from pydantic.dataclasses import dataclass


@dataclass
class HueBridgeDiscoverInfo:
    """Stores info from the discovery of a Hue bridge"""

    id: str
    internalipaddress: str
    port: int


@dataclass
class HueRoomLight:
    """Stores basic info about a light found in a room"""

    id: str
    name: str


@dataclass
class HueRoom:
    """Stores basic info about a room found via a bridge"""

    id: str
    name: str
    grouped_light_id: Optional[str]
    lights: list[HueRoomLight]

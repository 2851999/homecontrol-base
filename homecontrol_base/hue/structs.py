from pydantic.dataclasses import dataclass


@dataclass
class HueBridgeDiscoverInfo:
    """Stores info from the discovery of a Hue bridge"""

    id: str
    internalipaddress: str
    port: int

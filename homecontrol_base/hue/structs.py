from pydantic.dataclasses import dataclass


@dataclass
class HueBridgeDiscoverInfo:
    """Stores info from the discovery of a Hue bridge"""

    id: str
    internal_ip_address: str
    port: int

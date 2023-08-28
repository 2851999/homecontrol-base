from pydantic.dataclasses import dataclass


@dataclass
class BroadlinkDeviceDiscoverInfo:
    ip_address: str

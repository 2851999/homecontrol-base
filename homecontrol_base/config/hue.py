from pathlib import Path

from pydantic.dataclasses import dataclass

from homecontrol_base.config.base import BaseConfig


@dataclass
class HueConfigData:
    """Phillips Hue config data"""

    ca_cert: Path
    mDNS_discovery: bool  # Doesn't work on WSL for some reason (probably firewall related)


class HueConfig(BaseConfig[HueConfigData]):
    """All Midea config"""

    def __init__(self) -> None:
        super().__init__("hue.json", HueConfigData)

    @property
    def ca_cert(self) -> Path:
        return self._data.ca_cert

    @property
    def mDNS_discovery(self) -> bool:
        return self._data.mDNS_discovery

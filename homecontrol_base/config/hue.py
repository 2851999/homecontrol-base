from pathlib import Path

from pydantic.dataclasses import dataclass

from homecontrol_base.config.base import BaseConfig


@dataclass
class HueConfigData:
    """Phillip's Hue config data"""

    ca_cert: Path


class HueConfig(BaseConfig[HueConfigData]):
    """All Midea config"""

    def __init__(self) -> None:
        super().__init__("hue.json", HueConfigData)

    @property
    def ca_cert(self) -> Path:
        return self._data.ca_cert

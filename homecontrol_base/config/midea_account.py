from homecontrol_base.config.base import BaseConfig

from pydantic.dataclasses import dataclass


@dataclass
class MideaAccount:
    """Username and password for a Midea account"""

    username: str
    password: str


@dataclass
class MideaConfigData:
    """Midea account info for discovery"""

    account: MideaAccount


class MideaConfig(BaseConfig[MideaConfigData]):
    """All Midea config"""

    def __init__(self) -> None:
        super().__init__("midea.json", MideaConfigData)

    @property
    def account(self) -> MideaAccount:
        return self._data.account

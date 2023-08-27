import requests
from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.hue.exceptions import HueBridgeButtonNotPressedError


@dataclass
class HueBridgeDiscoverInfo:
    id: str
    internalipaddress: str
    port: int


class HueBridge:
    """Handles a Phillips Hue bridge"""

    DISCOVER_URL = "https://discovery.meethue.com/"

    @staticmethod
    def authenticate(
        name: str, discover_info: HueBridgeDiscoverInfo
    ) -> models.HueBridgeInfo:
        """Requests a new application key from a bridge

        When first run, will produce an error requesting the user to press
        the button to confirm authentication. The second time this is called
        authentication should be successful.

        Args:
            name (str): Name to label the bridge
            discover_info (str): Information from discovery

        Returns:
            models.HueBridgeInfo: Information required to connect to a bride

        Raises:
            HueBridgeButtonNotPressedError: When the button on the Hue bridge
                                            needs to be pressed
        """
        # Request a key
        response = requests.post(
            url=f"https://{discover_info.internalipaddress}/api",
            data={"devicetype": "homecontrol#base", "generateclientkey": True},
        )
        response.raise_for_status()

        response_json = response.json()
        if "error" in response_json and response_json["error"]["type"] == 101:
            # Need to press button
            raise HueBridgeButtonNotPressedError(
                "Please press the button on the Hue bridge with ip address "
                f"'{discover_info.internalipaddress}'"
            )
        elif "success" in response_json:
            # Now have a username and key
            return models.HueBridgeInfo(
                name=name,
                ip_address=discover_info.internalipaddress,
                identifier=discover_info.id,
                username=response_json["username"],
                client_key=response_json["clientkey"],
            )

        raise RuntimeError(
            f"Failed to authenticate Hue bridge with ip '{discover_info.internalipaddress}'"
        )

    @staticmethod
    def discover() -> list[HueBridgeDiscoverInfo]:
        """Discovers all Phillip's Hue bridges that are available on the
        current network"""

        response = requests.get(HueBridge.DISCOVER_URL)
        response.raise_for_status()
        bridges_dict = TypeAdapter(list[HueBridgeDiscoverInfo]).validate_python(
            response.json()
        )
        return bridges_dict

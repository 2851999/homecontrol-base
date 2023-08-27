from homecontrol_base.connection import BaseConnection
from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.hue.exceptions import HueBridgeButtonNotPressedError
from homecontrol_base.hue.session import HueBridgeSession


class HueBridgeAPIConnection(BaseConnection[HueBridgeSession]):
    def __init__(self, session: HueBridgeSession) -> None:
        super().__init__(session)

    def authenticate(self, name: str) -> models.HueBridgeInfo:
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
        discover_info = self._session.get_discover_info()

        # Request a key
        response = self._session.post(
            url="/api",
            json={"devicetype": "homecontrol#base", "generateclientkey": True},
        )
        response.raise_for_status()

        response_json = response.json()[0]
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
                port=discover_info.port,
                identifier=discover_info.id,
                username=response_json["username"],
                client_key=response_json["clientkey"],
            )

        raise RuntimeError(
            "Failed to authenticate Hue bridge with ip "
            f"'{discover_info.internalipaddress}', Response: {response_json}"
        )

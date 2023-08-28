from dataclasses import asdict, is_dataclass
import json
from typing import Type, TypeVar

from pydantic import TypeAdapter

from homecontrol_base.connection import BaseConnection
from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.hue.api.exceptions import check_response_for_error
from homecontrol_base.hue.api.schema import LightGet, LightPut
from homecontrol_base.hue.exceptions import HueBridgeButtonNotPressedError
from homecontrol_base.hue.session import HueBridgeSession

T = TypeVar("T")


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
                username=response_json["success"]["username"],
                client_key=response_json["success"]["clientkey"],
            )

        raise RuntimeError(
            "Failed to authenticate Hue bridge with ip "
            f"'{discover_info.internalipaddress}', Response: {response_json}"
        )

    def _get_resource(self, endpoint: str, resource_type: Type[T]) -> T:
        """Returns parsed data from a get request to an endpoint

        Args:
            endpoint (str): Endpoint to call
            resource_type (Type[T]): Type to parse to using pydantic

        Raises:
            HTTPError: When there is an error in the response
        """
        response = self._session.get(url=endpoint)
        check_response_for_error(response)
        return TypeAdapter(resource_type).validate_python(response.json()["data"])

    def _put_resource(self, endpoint: str, resource: T):
        """Put request of a resource to an endpoint

        Args:
            endpoint (str): Endpoint to call
            resource (T): Resource to put (Should be a dataclass that will be
                          converted - all values of None will be ignored)

        Raises:
            HTTPError: When there is an error in the response
        """

        if is_dataclass(resource):
            # Convert data
            data = asdict(
                resource, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
            )
        else:
            raise RuntimeError("Invalid resource type, should be a dataclass")

        response = self._session.put(url=endpoint, json=data)
        check_response_for_error(response)

    def get_lights(self) -> list[LightGet]:
        return self._get_resource("/clip/v2/resource/light", list[LightGet])

    def get_light(self, light_id: str) -> LightGet:
        return self._get_resource(
            f"/clip/v2/resource/light/{light_id}", list[LightGet]
        )[0]

    def put_light(self, light_id: str, data: LightPut):
        self._put_resource(f"/clip/v2/resource/light/{light_id}", data)

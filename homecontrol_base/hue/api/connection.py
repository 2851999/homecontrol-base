from dataclasses import asdict, is_dataclass
from typing import Type, TypeVar

from pydantic import TypeAdapter

from homecontrol_base.connection import BaseConnection
from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.hue.api.exceptions import check_response_for_error
from homecontrol_base.hue.api.schema import (
    GroupedLightGet,
    GroupedLightPut,
    LightGet,
    LightPut,
    ResourceIdentifierDelete,
    ResourceIdentifierPost,
    ResourceIdentifierPut,
    RoomGet,
    RoomPost,
    RoomPut,
    SceneGet,
    ScenePost,
    ScenePut,
)
from homecontrol_base.hue.exceptions import HueBridgeButtonNotPressedError
from homecontrol_base.hue.session import HueBridgeSession

T = TypeVar("T")


class HueBridgeAPIConnection(BaseConnection[HueBridgeSession]):
    def __init__(self, session: HueBridgeSession) -> None:
        super().__init__(session)

    def authenticate(self, name: str) -> models.HueBridgeInDB:
        """Requests a new application key from a bridge

        When first run, will produce an error requesting the user to press
        the button to confirm authentication. The second time this is called
        authentication should be successful.

        Args:
            name (str): Name to label the bridge
            discover_info (str): Information from discovery

        Returns:
            models.HueBridgeInDB: Information required to connect to a bride

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
                f"'{discover_info.internal_ip_address}'"
            )
        elif "success" in response_json:
            # Now have a username and key
            return models.HueBridgeInDB(
                name=name,
                ip_address=discover_info.internal_ip_address,
                port=discover_info.port,
                identifier=discover_info.id,
                username=response_json["success"]["username"],
                client_key=response_json["success"]["clientkey"],
            )

        raise RuntimeError(
            "Failed to authenticate Hue bridge with ip "
            f"'{discover_info.internal_ip_address}', Response: {response_json}"
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

    def _convert_resource_to_dict(self, resource: T) -> dict:
        """Converts a resource (dataclass) into a dictionary

        All values of None will be ignored

        Args:
            resource (T): Resource to convert

        Returns:
            dict: Dictionary of data

        Raises:
            TypeError: If the resource type is invalid
        """
        if is_dataclass(resource):
            # Convert data
            return asdict(
                resource, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
            )
        else:
            raise TypeError("Invalid resource type, should be a dataclass")

    def _put_resource(self, endpoint: str, resource: T) -> ResourceIdentifierPut:
        """Put request of a resource to an endpoint

        Args:
            endpoint (str): Endpoint to call
            resource (T): Resource to put (Should be a dataclass that will be
                          converted)

        Raises:
            TypeError: If the resource type is invalid
            HTTPError: When there is an error in the response
        """

        response = self._session.put(
            url=endpoint,
            json=self._convert_resource_to_dict(resource),
        )
        check_response_for_error(response)
        return TypeAdapter(list[ResourceIdentifierPut]).validate_python(
            response.json()["data"]
        )[0]

    def _post_resource(self, endpoint: str, resource: T) -> ResourceIdentifierPost:
        """Post request of a resource to an endpoint

        Args:
            endpoint (str): Endpoint to call
            resource (T): Resource to put (Should be a dataclass that will be
                          converted)

        Raises:
            TypeError: If the resource type is invalid
            HTTPError: When there is an error in the response
        """
        response = self._session.post(
            url=endpoint,
            json=self._convert_resource_to_dict(resource),
        )
        check_response_for_error(response)
        return TypeAdapter(list[ResourceIdentifierPost]).validate_python(
            response.json()["data"]
        )[0]

    def _delete_resource(self, endpoint: str) -> ResourceIdentifierDelete:
        """Delete request of a resource to an endpoint

        Args:
            endpoint (str): Endpoint to call

        Raises:
            HTTPError: When there is an error in the response
        """
        response = self._session.delete(url=endpoint)
        check_response_for_error(response)
        return TypeAdapter(list[ResourceIdentifierDelete]).validate_python(
            response.json()["data"]
        )[0]

    # -------------------------------- Lights --------------------------------

    def get_lights(self) -> list[LightGet]:
        return self._get_resource("/clip/v2/resource/light", list[LightGet])

    def get_light(self, light_id: str) -> LightGet:
        return self._get_resource(
            f"/clip/v2/resource/light/{light_id}", list[LightGet]
        )[0]

    def put_light(self, light_id: str, data: LightPut) -> ResourceIdentifierPut:
        return self._put_resource(f"/clip/v2/resource/light/{light_id}", data)

    # -------------------------------- Scenes --------------------------------

    def get_scenes(self) -> list[SceneGet]:
        return self._get_resource("/clip/v2/resource/scene", list[SceneGet])

    def get_scene(self, scene_id: str) -> SceneGet:
        return self._get_resource(
            f"/clip/v2/resource/scene/{scene_id}", list[SceneGet]
        )[0]

    def put_scene(self, scene_id: str, data: ScenePut) -> ResourceIdentifierPut:
        return self._put_resource(f"/clip/v2/resource/scene/{scene_id}", data)

    def post_scene(self, data: ScenePost) -> ResourceIdentifierPost:
        return self._post_resource("/clip/v2/resource/scene", data)

    def delete_scene(self, scene_id: str) -> ResourceIdentifierDelete:
        return self._delete_resource(f"/clip/v2/resource/scene/{scene_id}")

    # -------------------------------- Rooms --------------------------------
    def get_rooms(self) -> list[RoomGet]:
        return self._get_resource("/clip/v2/resource/room", list[RoomGet])

    def get_room(self, room_id: str) -> RoomGet:
        return self._get_resource(f"/clip/v2/resource/room/{room_id}", list[RoomGet])[0]

    def put_room(self, room_id: str, data: RoomPut) -> ResourceIdentifierPut:
        return self._put_resource(f"/clip/v2/resource/room/{room_id}", data)

    def post_room(self, data: RoomPost) -> ResourceIdentifierPost:
        return self._post_resource("/clip/v2/resource/room", data)

    def delete_room(self, room_id: str) -> ResourceIdentifierDelete:
        return self._delete_resource(f"/clip/v2/resource/room/{room_id}")

    # -------------------------------- GroupedLights --------------------------------
    def get_grouped_lights(self) -> list[GroupedLightGet]:
        return self._get_resource(
            "/clip/v2/resource/grouped_light", list[GroupedLightGet]
        )

    def get_grouped_light(self, grouped_light_id: str) -> GroupedLightGet:
        return self._get_resource(
            f"/clip/v2/resource/grouped_light/{grouped_light_id}", list[GroupedLightGet]
        )[0]

    def put_grouped_light(
        self, grouped_light_id: str, data: GroupedLightPut
    ) -> ResourceIdentifierPut:
        return self._put_resource(
            f"/clip/v2/resource/grouped_light/{grouped_light_id}", data
        )

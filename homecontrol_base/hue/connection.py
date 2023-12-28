from typing import Optional

from homecontrol_base.connection import BaseConnection
from homecontrol_base.hue.api.colour import HueColour
from homecontrol_base.hue.api.connection import HueBridgeAPIConnection
from homecontrol_base.hue.api.schema import (
    ColorPut,
    ColorTemperaturePut,
    DimmingPut,
    GroupedLightPut,
    LightPut,
    OnPut,
    Recall,
    RoomGet,
    ScenePut,
)
from homecontrol_base.hue.session import HueBridgeSession
from homecontrol_base.hue.structs import (
    HueRoom,
    HueRoomGroupedLightState,
    HueRoomLight,
    HueRoomLightState,
    HueRoomSceneState,
    HueRoomState,
    HueRoomStateUpdate,
)


class HueBridgeConnection(BaseConnection[HueBridgeSession]):
    _api_connection: HueBridgeAPIConnection

    def __init__(self, api_connection: HueBridgeAPIConnection) -> None:
        super().__init__(api_connection._session)

        self._api_connection = api_connection

    def _get_room(self, hue_room: RoomGet) -> HueRoom:
        """Constructs a HueRoom by performing the required requests to a Hue bridge"""

        # Attempt to find a grouped light service
        grouped_light_id: Optional[str] = None
        for service in hue_room.services:
            if service.rtype == "grouped_light":
                grouped_light_id = service.rid
                break

        # Locate all lights
        lights: dict[str, HueRoomLight] = {}
        for child in hue_room.children:
            if child.rtype == "device":
                device = self._api_connection.get_device(child.rid)
                for service in device.services:
                    if service.rtype == "light":
                        lights[service.rid] = HueRoomLight(name=device.metadata.name)
                        break

        return HueRoom(
            id=hue_room.id,
            name=hue_room.metadata.name,
            grouped_light_id=grouped_light_id,
            lights=lights,
        )

    def get_rooms(self) -> list[HueRoom]:
        """Returns a list of HueRoom's"""
        return [self._get_room(room) for room in self._api_connection.get_rooms()]

    def get_room(self, room_id: str) -> HueRoom:
        """Returns a HueRoom with a given id"""
        return self._get_room(self._api_connection.get_room(room_id))

    def get_room_state(self, room_id: str) -> HueRoomState:
        """Returns the state of a HueRoom"""

        # Obtain the room itself
        hue_room = self._api_connection.get_room(room_id)
        room = self._get_room(hue_room)

        # Obtain the grouped light state
        grouped_light_state = self._api_connection.get_grouped_light(
            room.grouped_light_id
        )

        # Obtain the states of each light
        light_states: dict[str, HueRoomLightState] = {}

        for light_id, light in room.lights.items():
            light_state = self._api_connection.get_light(light_id=light_id)

            light_states[light_id] = HueRoomLightState(
                name=light.name,
                on=light_state.on.on,
                brightness=light_state.dimming.brightness
                if light_state.dimming is not None
                else None,
                colour_temperature=light_state.color_temperature.mirek
                if light_state.color_temperature is not None
                else None,
                colour=HueColour.from_xy(light_state.color.xy)
                if light_state.color is not None
                else None,
            )

        # Locate all scenes
        scenes: dict[str, HueRoomSceneState] = {}
        for scene in self._api_connection.get_scenes():
            if scene.group.rid == hue_room.id:
                scenes[scene.id] = HueRoomSceneState(
                    name=scene.metadata.name, status=scene.status.active
                )

        return HueRoomState(
            grouped_light=HueRoomGroupedLightState(
                on=grouped_light_state.on.on
                if grouped_light_state.on is not None
                else None,
                brightness=grouped_light_state.dimming.brightness
                if grouped_light_state.dimming is not None
                else None
                if grouped_light_state.dimming
                else None,
            ),
            lights=light_states,
            scenes=scenes,
        )

    def set_room_state(
        self, room_id: str, update_data: HueRoomStateUpdate
    ) -> HueRoomState:
        """Updates the state of a HueRoom

        Args:
            room_id (str): ID of the HueRoom to update
            update_data (HueRoomStateUpdate): Update data to assign
        """

        # Obtain the room itself
        room = self._get_room(self._api_connection.get_room(room_id))

        # Check what needs updating and update them
        if update_data.grouped_light is not None:
            grouped_light_put = GroupedLightPut(
                on=OnPut(on=update_data.grouped_light.on)
                if update_data.grouped_light.on is not None
                else None,
                dimming=DimmingPut(brightness=update_data.grouped_light.brightness)
                if update_data.grouped_light.brightness is not None
                else None,
            )
            self._api_connection.put_grouped_light(
                room.grouped_light_id, grouped_light_put
            )
        if update_data.lights is not None:
            for light_id, light_update_data in update_data.lights.items():
                light_put = LightPut(
                    on=OnPut(on=light_update_data.on)
                    if light_update_data.on is not None
                    else None,
                    dimming=DimmingPut(brightness=light_update_data.brightness)
                    if light_update_data.brightness is not None
                    else None,
                    color_temperature=ColorTemperaturePut(
                        mirek=light_update_data.colour_temperature
                    )
                    if light_update_data.colour_temperature is not None
                    else None,
                    color=ColorPut(xy=light_update_data.colour.to_xy())
                    if light_update_data.colour is not None
                    else None,
                )
                self._api_connection.put_light(light_id, light_put)
        if update_data.scene is not None:
            self._api_connection.put_scene(
                update_data.scene, ScenePut(recall=Recall(action="active"))
            )

        return self.get_room_state(room_id)

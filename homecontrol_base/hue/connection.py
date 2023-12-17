from typing import Optional

from homecontrol_base.connection import BaseConnection
from homecontrol_base.hue.api.connection import HueBridgeAPIConnection
from homecontrol_base.hue.api.schema import RoomGet
from homecontrol_base.hue.session import HueBridgeSession
from homecontrol_base.hue.structs import HueRoom, HueRoomLight


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
        lights: list[HueRoomLight] = []
        for child in hue_room.children:
            if child.rtype == "device":
                device = self._api_connection.get_device(child.rid)
                for service in device.services:
                    if service.rtype == "light":
                        lights.append(
                            HueRoomLight(id=service.rid, name=device.metadata.name)
                        )
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

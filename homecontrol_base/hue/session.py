from pathlib import Path
from typing import Union

from requests.adapters import HTTPAdapter

from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.hue.structs import HueBridgeDiscoverInfo
from homecontrol_base.session import SessionWithBaseURL


class HostNameIgnoringAdapter(HTTPAdapter):
    """Custom adaptor that ignores the hostname in SSL cert auth

    Phillips Hue Bridge's currently have certs lacking subjectAltName, which
    breaks past urllib3 2.x.x. This is required until fixed. Otherwise would
    only need to use HostHeaderSSLAdapter from requests_toolbelt with
    {"Host": bridge_identifier} in the headers
    """

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        return super().init_poolmanager(
            connections, maxsize, block, assert_hostname=False, **pool_kwargs
        )


class HueBridgeSession(SessionWithBaseURL):
    """Handles a connection to a Phillips Hue bridge session"""

    _connection_info: Union[HueBridgeDiscoverInfo, models.HueBridgeInfo]

    def __init__(
        self,
        connection_info: Union[HueBridgeDiscoverInfo, models.HueBridgeInfo],
        ca_cert: Path,
    ) -> None:
        """Constructor

        Args:
            connection_info (Union[HueBridgeDiscoverInfo, models.HueBridgeInfo]):
                            Info for connecting to the bridge
            ca_cert (Path): Path to the Hue bridge certificate required for a
                            HTTPS connection
        """

        self._connection_info = connection_info
        # Setup for appropriate info
        if isinstance(connection_info, HueBridgeDiscoverInfo):
            # No auth
            base_url = (
                f"https://{connection_info.internalipaddress}:{connection_info.port}"
            )
            auth = False
        else:
            # Auth
            base_url = f"https://{connection_info.ip_address}:{connection_info.port}"
            auth = True

        super().__init__(base_url)

        # Auth setup
        if auth:
            self.headers.update({"hue-application-key": connection_info.username})
        self.mount("https://", HostNameIgnoringAdapter())
        self.verify = ca_cert

    def get_discover_info(self) -> HueBridgeDiscoverInfo:
        """Returns discover info (only applicable if haven't authenticated yet)

        Raises:
            RuntimeError: If the connection info given isn't from discovery
        """
        if isinstance(self._connection_info, HueBridgeDiscoverInfo):
            return self._connection_info
        raise RuntimeError(
            "Cannot get HueBridgeDiscoverInfo from this session as already authenticated"
        )

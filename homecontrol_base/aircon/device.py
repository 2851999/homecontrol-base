import asyncio

from msmart.scanner import MideaDiscovery

from homecontrol_base.config.midea import MideaAccount
from homecontrol_base.database import models
from homecontrol_base.exceptions import DeviceConnectionError


class ACDevice:
    """Class for handling an air conditioning device"""

    @staticmethod
    def discover(name: str, ip_address: str, account: MideaAccount) -> models.ACDevice:
        """Attempts to make a connection with an air conditioning unit given
        it's ip address and returns the relevant details to make a connection

        Args:
            name (str): Name to give the device
            ip_address (str): IP address of the device
            account (MideaAccount): Account to use for the discovery

        Returns:
            models.ACDevice: Information for connecting to the device

        Raises:
            DeviceConnectionError: When an error occurs while attempting to
                                   connect to the device
        """

        found_devices = None
        try:
            discovery = MideaDiscovery(
                account=account.username, password=account.password, amount=1
            )
            loop = asyncio.new_event_loop()
            found_devices = loop.run_until_complete(discovery.get(ip_address))
            loop.close()
        except Exception as err:
            raise DeviceConnectionError(
                "An error occurred while attempting to discover an air "
                f"conditioning unit at {ip_address}"
            )

        if found_devices:
            # Only looked for one anyway
            found_device = list(found_devices)[0]

            # Validate auth data was obtained correctly
            if found_device.key is None or found_device.token is None:
                raise DeviceConnectionError(
                    "Unable to obtain authentication for air conditioning "
                    f"unit at {ip_address}"
                )

            # Return the required info
            return models.ACDevice(
                name=name,
                ip_address=ip_address,
                identifier=found_device.id,
                key=found_device.key,
                token=found_device.token,
            )
        raise DeviceConnectionError(
            f"Unable to find the air conditioning unit with ip {ip_address}"
        )

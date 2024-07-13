import asyncio

from msmart.device.AC.device import AirConditioner
from msmart.discover import Discover
from msmart.lan import AuthenticationError

from homecontrol_base.aircon.exceptions import (
    ACAuthenticationError,
    ACInvalidStateError,
)
from homecontrol_base.aircon.state import ACDeviceState
from homecontrol_base.config.midea import MideaAccount
from homecontrol_base.database.homecontrol_base import models
from homecontrol_base.exceptions import DeviceConnectionError, DeviceNotFoundError


class ACDevice:
    """Class for handling an air conditioning device"""

    _device_info: models.ACDeviceInfoInDB
    _device: AirConditioner

    # Whether to toggle the display the next time the state is applied
    _should_toggle_display: bool

    def __init__(self, device_info: models.ACDeviceInfoInDB):
        """Initialises and authenticates the device

        Args:
            device_info (models.ACDeviceInfoInDB): Device authentication info
        """

        # Connect to the device
        self._device_info = device_info
        self._device = AirConditioner(
            device_info.ip_address, device_info.identifier, 6444
        )

        self._should_toggle_display = False

    async def initialise(self):
        """Initialises and authenticates the device

        Should be called immediately after __init__

        Raises:
            ACAuthenticationError: If authentication fails
        """

        # Attempt authentication up to 3 times (can often fail temporarily)
        for retry in range(0, 3):
            try:
                await self._device.authenticate(
                    token=self._device_info.token, key=self._device_info.key
                )
                break
            except AuthenticationError as err:
                if retry == 2:
                    raise ACAuthenticationError(
                        f"Failed to authenticate with AC unit {self._device_info.identifier} after retrying 3 times"
                    ) from err
                else:
                    await asyncio.sleep(1)

        await self._device.get_capabilities()

    def _get_current_state(self) -> ACDeviceState:
        """Returns the current state of the device"""
        return ACDeviceState(
            power=self._device.power_state,
            target_temperature=self._device.target_temperature,
            operational_mode=self._device.operational_mode,
            fan_speed=self._device.fan_speed,
            swing_mode=self._device.swing_mode,
            eco_mode=self._device.eco_mode,
            turbo_mode=self._device.turbo_mode,
            fahrenheit=self._device.fahrenheit,
            indoor_temperature=self._device.indoor_temperature,
            outdoor_temperature=self._device.outdoor_temperature,
            display_on=self._device.display_on if self._device.power_state else False,
            prompt_tone=self._device.beep,
        )

    def _assign_state(self, state: ACDeviceState):
        """Assigns a given state to the device"""
        self._device.power_state = state.power
        self._device.target_temperature = state.target_temperature
        self._device.operational_mode = state.operational_mode
        self._device.fan_speed = state.fan_speed
        self._device.swing_mode = state.swing_mode
        self._device.eco_mode = state.eco_mode
        self._device.turbo_mode = state.turbo_mode
        self._device.fahrenheit = state.fahrenheit
        self._device.beep = state.prompt_tone
        self._should_toggle_display = self._device.display_on is not state.display_on

    def _validate_state(self, state: ACDeviceState):
        """Checks that the given state is valid (for use before it is sent to the device)

        Raises:
            ACInvalidStateError: If the given state is invalid
        """
        if state.eco_mode and state.turbo_mode:
            raise ACInvalidStateError(
                "Cannot have both 'eco_mode' and 'turbo_mode' True at the same time"
            )
        if not 16 <= state.target_temperature <= 30:
            raise ACInvalidStateError(
                f"'target_temperature' of {state.target_temperature} must be between 16 and 30"
            )

    async def _refresh_state(self, current_retry: int = 0):
        """Attempts to refresh the current state

        Retries 3 times in the event something appears to go wrong
        Raises:
            DeviceConnectionError: If the refresh repeatedly fails
        """
        await self._device.refresh()

        # Check if anything appears wrong
        if self._device.indoor_temperature is None:
            if current_retry < 3:
                await self._refresh_state(current_retry=current_retry + 1)
            else:
                raise DeviceConnectionError(
                    f"An error occurred while attempting to refresh the state of an AC unit {self._device_info.identifier}"
                )

    async def get_state(self) -> ACDeviceState:
        """Refreshes the device and returns it's current state

        Returns:
            ACDeviceState: The current device state
        """
        # Units sometimes return 0 when this is not actually accurate,
        # refresh twice in such cases
        await self._refresh_state()
        if (
            self._device.indoor_temperature == 0
            and self._device.outdoor_temperature == 0
        ):
            await self._refresh_state()

        return self._get_current_state()

    async def _apply_state(self, current_retry: int = 0):
        """Attempts to apply the currently assigned device state

        Retries 3 times in the event of an error

        Raises:
            DeviceConnectionError: If the connection repeatedly fails
        """
        try:
            await self._device.apply()
            if self._should_toggle_display:
                await self._device.toggle_display()
        except UnboundLocalError as err:
            if current_retry < 3:
                self._apply_state(current_retry=current_retry + 1)
            else:
                raise DeviceConnectionError(
                    f"An error occurred while attempting to apply a state to the AC unit {self._device_info.identifier}"
                ) from err

    async def set_state(self, state: ACDeviceState):
        """Attempts to assign the device state

        Raises:
            ACInvalidStateError: If the given state is invalid
        """
        self._validate_state(state)
        self._assign_state(state)

        # Attempt to apply the state
        await self._apply_state()

    @property
    def info(self) -> models.ACDeviceInfoInDB:
        """Returns information about the device"""
        return self._device_info

    @staticmethod
    async def discover(
        name: str, ip_address: str, account: MideaAccount
    ) -> models.ACDeviceInfoInDB:
        """Attempts to make a connection with an air conditioning unit given
        it's ip address and returns the relevant details to make a connection

        Args:
            name (str): Name to give the device
            ip_address (str): IP address of the device
            account (MideaAccount): Account to use for the discovery

        Returns:
            models.ACDeviceInfoInDB: Information for connecting to the device

        Raises:
            DeviceConnectionError: When an error occurs while attempting to
                                   connect to the device
            DeviceNotFoundError: When the device isn't found
        """

        found_devices = None
        try:
            # Try a max of 3 times
            attempts = 0
            while not found_devices and attempts < 3:
                found_devices = await Discover.discover(
                    target=ip_address,
                    account=account.username,
                    password=account.password,
                )
                attempts += 1
        except Exception as err:
            raise DeviceConnectionError(
                "An error occurred while attempting to discover an air "
                f"conditioning unit at {ip_address}"
            ) from err

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
            return models.ACDeviceInfoInDB(
                name=name,
                ip_address=ip_address,
                identifier=found_device.id,
                key=found_device.key,
                token=found_device.token,
            )
        raise DeviceNotFoundError(
            f"Unable to find the air conditioning unit with ip address '{ip_address}'"
        )

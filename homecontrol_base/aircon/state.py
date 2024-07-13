from enum import IntEnum
from typing import Annotated

from msmart.device.AC.device import AirConditioner
from pydantic import BeforeValidator
from pydantic.dataclasses import dataclass


class ACDeviceMode(IntEnum):
    """Wrapper for air conditioning modes"""

    AUTO = AirConditioner.OperationalMode.AUTO  # 1
    COOL = AirConditioner.OperationalMode.COOL  # 2
    DRY = AirConditioner.OperationalMode.DRY  # 3
    HEAT = AirConditioner.OperationalMode.HEAT  # 4
    FAN = AirConditioner.OperationalMode.FAN_ONLY  # 5


class ACDeviceFanSpeed(IntEnum):
    """Wrapper for air conditioning fan speeds"""

    AUTO = AirConditioner.FanSpeed.AUTO  # 102
    HIGH = AirConditioner.FanSpeed.HIGH  # 100
    MEDIUM = AirConditioner.FanSpeed.MEDIUM  # 80
    LOW = AirConditioner.FanSpeed.LOW  # 40
    SILENT = AirConditioner.FanSpeed.SILENT  # 20


class ACDeviceSwingMode(IntEnum):
    """Wrapper for air conditioning swing modes"""

    OFF = AirConditioner.SwingMode.OFF  # 0x0, 0
    VERTICAL = AirConditioner.SwingMode.VERTICAL  # 0xC, 12
    HORIZONTAL = AirConditioner.SwingMode.HORIZONTAL  # 0x3, 3
    BOTH = AirConditioner.SwingMode.BOTH  # 0xF, 14


def _fan_speed_validator(value: int) -> ACDeviceFanSpeed:
    """Validator for fan speed assignment

    For a mode such as Dry - the fan speed can be 101 in my case, old
    msmart would return default of Auto, but msmart-ng just returns 101
    so recreate the old behaviour here to avoid validation errors
    """
    if value in set(speed.value for speed in ACDeviceFanSpeed):
        return value
    else:
        return ACDeviceFanSpeed.AUTO


@dataclass
class ACDeviceState:
    """For storing the state of an air conditioning device"""

    # Read and write
    power: bool
    target_temperature: float
    operational_mode: ACDeviceMode
    fan_speed: Annotated[ACDeviceFanSpeed, BeforeValidator(_fan_speed_validator)]
    swing_mode: ACDeviceSwingMode
    eco_mode: bool
    turbo_mode: bool
    fahrenheit: bool
    display_on: bool

    # Read only
    indoor_temperature: float
    outdoor_temperature: float

    # Write only
    prompt_tone: bool

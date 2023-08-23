from enum import IntEnum

from msmart.device import air_conditioning
from pydantic.dataclasses import dataclass


class ACDeviceMode(IntEnum):
    """Wrapper for air conditioning modes"""

    AUTO = air_conditioning.operational_mode_enum.auto  # 1
    COOL = air_conditioning.operational_mode_enum.cool  # 2
    DRY = air_conditioning.operational_mode_enum.dry  # 3
    HEAT = air_conditioning.operational_mode_enum.heat  # 4
    FAN = air_conditioning.operational_mode_enum.fan_only  # 5


class ACDeviceFanSpeed(IntEnum):
    """Wrapper for air conditioning fan speeds"""

    AUTO = air_conditioning.fan_speed_enum.Auto  # 102
    FULL = air_conditioning.fan_speed_enum.Full  # 100
    MEDIUM = air_conditioning.fan_speed_enum.Medium  # 80
    LOW = air_conditioning.fan_speed_enum.Low  # 40
    SILENT = air_conditioning.fan_speed_enum.Silent  # 20


class ACDeviceSwingMode(IntEnum):
    """Wrapper for air conditioning swing modes"""

    OFF = air_conditioning.swing_mode_enum.Off  # 0x0, 0
    VERTICAL = air_conditioning.swing_mode_enum.Vertical  # 0xC, 12
    HORIZONTAL = air_conditioning.swing_mode_enum.Horizontal  # 0x3, 3
    BOTH = air_conditioning.swing_mode_enum.Both  # 0xF, 14


@dataclass
class ACDeviceState:
    """For storing the state of an air conditioning device"""

    # Read and write
    power: bool
    target_temperature: float
    operational_mode: ACDeviceMode
    fan_speed: ACDeviceFanSpeed
    swing_mode: ACDeviceSwingMode
    eco_mode: bool
    turbo_mode: bool
    fahrenheit: bool

    # Read only
    indoor_temperature: float
    outdoor_temperature: float
    display_on: bool

    # Write only
    prompt_tone: bool

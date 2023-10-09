from enum import IntEnum

from msmart.device.AC.device import AirConditioner
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
    FULL = AirConditioner.FanSpeed.FULL  # 100
    MEDIUM = AirConditioner.FanSpeed.MEDIUM  # 80
    LOW = AirConditioner.FanSpeed.LOW  # 40
    SILENT = AirConditioner.FanSpeed.SILENT  # 20


class ACDeviceSwingMode(IntEnum):
    """Wrapper for air conditioning swing modes"""

    OFF = AirConditioner.SwingMode.OFF  # 0x0, 0
    VERTICAL = AirConditioner.SwingMode.VERTICAL  # 0xC, 12
    HORIZONTAL = AirConditioner.SwingMode.HORIZONTAL  # 0x3, 3
    BOTH = AirConditioner.SwingMode.BOTH  # 0xF, 14


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

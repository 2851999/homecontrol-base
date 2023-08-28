from typing import Literal, Optional

from pydantic.dataclasses import dataclass


@dataclass
class OwnerGet:
    rid: str
    rtype: str


@dataclass
class OnGet:
    on: bool


@dataclass
class DimmingGet:
    brightness: float
    min_dim_level: Optional[float] = None


@dataclass
class MirekSchemaGet:
    mirek_minimum: int
    mirek_maximum: int


@dataclass
class ColorTemperatureGet:
    mirek: Optional[int]
    mirek_valid: bool
    mirek_schema: MirekSchemaGet


@dataclass
class XYGet:
    x: float
    y: float


@dataclass
class GamutGet:
    red: XYGet
    green: XYGet
    blue: XYGet


@dataclass
class ColorGet:
    xy: XYGet
    gamut_type: Literal["A", "B", "C", "other"]
    gamut: Optional[GamutGet] = None


@dataclass
class DynamicsGet:
    status: Literal["dynamic_palette", "none"]
    status_values: list[str]
    speed: float
    speed_valid: bool


@dataclass
class AlertGet:
    action_values: list[str]


@dataclass
class StatusGet:
    signal: Literal["no_signal", "on_off"]
    estimated_end: str


@dataclass
class SignalingGet:
    status: Optional[StatusGet] = None


@dataclass
class GradientColorGet:
    xy: XYGet


@dataclass
class GradientPointGet:
    color: GradientColorGet


@dataclass
class GradientGet:
    points: list[GradientPointGet]
    mode: str  # Literal["interpolated_palette", "interpolated_palette_mirrored", "random_pixelated"]
    points_capable: int
    mode_values: list[str]
    pixel_count: Optional[int] = None


@dataclass
class EffectsGet:
    status_values: list[str]
    status: str  # Literal["sparkle", "fire", "candle", "no_effect"]
    effect_values: list[str]
    effect: Optional[str] = None  # Literal["sparkle", "fire", "candle", "no_effect"]


@dataclass
class TimedEffectsGet:
    effect: str  # Literal["sunrise", "no_effect"]
    status_values: list[str]
    status: str  # Literal["sunrise", "no_effect"]
    effect_values: list[str]
    duration: Optional[int] = None


@dataclass
class PowerupOnGet:
    mode: str  # Literal["on", "toggle", "previous"]
    on: Optional[OnGet] = None


@dataclass
class PowerupDimmingDimmingGet:
    brightness: float


@dataclass
class PowerupDimmingGet:
    mode: str  # Literal["dimming", "previous"]
    dimming: Optional[PowerupDimmingDimmingGet] = None


@dataclass
class PowerupColorTemperatureGet:
    mirek: int


@dataclass
class PowerupColorColorGet:
    xy: XYGet


@dataclass
class PowerupColorGet:
    mode: str  # Literal["color_temperature", "color", "previous"]
    color_temperature: Optional[PowerupColorTemperatureGet] = None
    color: Optional[PowerupColorColorGet] = None


@dataclass
class PowerupGet:
    preset: str  # Literal["safety", "powerfail", "last_on_state", "custom"]
    configured: bool
    on: PowerupOnGet
    dimming: Optional[PowerupDimmingGet] = None
    color: Optional[PowerupColorGet] = None


@dataclass
class LightGet:
    type: str
    id: str
    owner: OwnerGet
    # metadata - deprecated
    on: OnGet
    mode: str  # Literal["normal", "streaming"]
    id_v1: Optional[str] = None
    dimming: Optional[DimmingGet] = None
    color_temperature: Optional[ColorTemperatureGet] = None
    color: Optional[ColorGet] = None
    dynamics: Optional[DynamicsGet] = None
    alert: Optional[AlertGet] = None
    signaling: Optional[SignalingGet] = None
    gradient: Optional[GradientGet] = None
    effects: Optional[EffectsGet] = None
    timed_effects: Optional[TimedEffectsGet] = None
    powerup: Optional[PowerupGet] = None

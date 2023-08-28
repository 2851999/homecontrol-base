from typing import Literal, Optional

from pydantic.dataclasses import dataclass


@dataclass
class ResourceIdentifierDelete:
    rid: str
    rtype: str


# -------------------------------- LightGet --------------------------------


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
class ColorGetXY:
    xy: XYGet


@dataclass
class GradientPointGet:
    color: ColorGetXY


@dataclass
class GradientGet:
    points: list[GradientPointGet]
    mode: Literal[
        "interpolated_palette", "interpolated_palette_mirrored", "random_pixelated"
    ]
    points_capable: int
    mode_values: list[str]
    pixel_count: Optional[int] = None


@dataclass
class EffectsGet:
    status_values: list[str]
    status: Literal["sparkle", "fire", "candle", "no_effect"]
    effect_values: list[str]
    effect: Optional[Literal["sparkle", "fire", "candle", "no_effect"]] = None


@dataclass
class TimedEffectsGet:
    effect: Literal["sunrise", "no_effect"]
    status_values: list[str]
    status: Literal["sunrise", "no_effect"]
    effect_values: list[str]
    duration: Optional[int] = None


@dataclass
class PowerupOnGet:
    mode: Literal["on", "toggle", "previous"]
    on: Optional[OnGet] = None


@dataclass
class DimmingGetBrightness:
    brightness: float


@dataclass
class PowerupDimmingGet:
    mode: Literal["dimming", "previous"]
    dimming: Optional[DimmingGetBrightness] = None


@dataclass
class ColorTemperatureGetMirek:
    mirek: int


@dataclass
class PowerupColorGet:
    mode: Literal["color_temperature", "color", "previous"]
    color_temperature: Optional[ColorTemperatureGetMirek] = None
    color: Optional[ColorGetXY] = None


@dataclass
class PowerupGet:
    preset: Literal["safety", "powerfail", "last_on_state", "custom"]
    configured: bool
    on: PowerupOnGet
    dimming: Optional[PowerupDimmingGet] = None
    color: Optional[PowerupColorGet] = None


@dataclass
class LightGet:
    type: Literal["light"]
    id: str
    owner: OwnerGet
    # metadata - deprecated
    on: OnGet
    mode: Literal["normal", "streaming"]
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


# -------------------------------- LightPut --------------------------------


@dataclass
class MetadataPut:
    name: Optional[str] = None
    archetype: Optional[str] = None


@dataclass
class OnPut:
    on: Optional[bool] = None


@dataclass
class DimmingPut:
    brightness: Optional[float] = None


@dataclass
class DimmingDeltaPut:
    action: Literal["up", "down", "stop"]
    brightness_delta: Optional[float] = None


@dataclass
class ColorTemperaturePut:
    mirek: Optional[int] = None


@dataclass
class ColorTemperatureDeltaPut:
    action: Literal["up", "down", "stop"]
    mirek_delta: Optional[int]


@dataclass
class XYPut:
    x: float
    y: float


@dataclass
class ColorPut:
    xy: Optional[XYPut] = None


@dataclass
class DynamicsPut:
    duration: Optional[int] = None
    speed: Optional[float] = None


@dataclass
class AlertPut:
    action: str


@dataclass
class GradientPointPut:
    color: ColorPut


@dataclass
class GradientPut:
    points: list[GradientPointPut]
    mode: Literal[
        "interpolated_palette", "interpolated_palette_mirrored", "random_pixelated"
    ]


@dataclass
class EffectsPut:
    effect: Optional[Literal["sparkle", "fire", "candle", "no_effect"]] = None


@dataclass
class TimedEffectsPut:
    effect: Optional[Literal["sunrise", "no_effect"]] = None
    duration: Optional[int] = None


@dataclass
class PowerupOnPut:
    mode: Literal["on", "toggle", "previous"]
    on: Optional[OnPut] = None


@dataclass
class PowerupDimmingDimmingPut:
    brightness: Optional[float] = None


@dataclass
class PowerupDimmingPut:
    mode: Literal["dimming", "previous"]
    dimming: Optional[PowerupDimmingDimmingPut] = None


@dataclass
class PowerupColorPut:
    mode: Literal["color_temperature", "color", "previous"]
    color_temperature: Optional[ColorTemperaturePut] = None
    color: Optional[ColorPut] = None


@dataclass
class PowerupPut:
    preset: Literal["safety", "powerfail", "last_on_state", "custom"]
    on: Optional[PowerupOnPut] = None
    dimming: Optional[PowerupDimmingPut] = None
    color: Optional[PowerupColorPut] = None


@dataclass
class LightPut:
    type: Optional[Literal["light"]] = None
    metadata: Optional[MetadataPut] = None
    on: Optional[OnPut] = None
    dimming: Optional[DimmingPut] = None
    dimming_delta: Optional[DimmingDeltaPut] = None
    color_temperature: Optional[ColorTemperaturePut] = None
    color_temperature_delta: Optional[ColorTemperatureDeltaPut] = None
    color: Optional[ColorPut] = None
    dynamics: Optional[DynamicsPut] = None
    alert: Optional[AlertPut] = None
    gradient: Optional[GradientPut] = None
    effects: Optional[EffectsPut] = None
    timed_effects: Optional[TimedEffectsPut] = None
    powerup: Optional[PowerupPut] = None


# -------------------------------- SceneGet --------------------------------


@dataclass
class ActionTargetGet:
    rid: str
    rtype: str


@dataclass
class ActionActionGradientGet:
    points: list[GradientPointGet]
    mode: Literal[
        "interpolated_palette", "interpolated_palette_mirrored", "random_pixelated"
    ]


@dataclass
class ActionActionEffectsGet:
    effect: Literal["sparkle", "fire", "candle", "no_effect"]


@dataclass
class ActionActionDynamicsGet:
    duration: int


@dataclass
class ActionActionGet:
    on: Optional[OnGet] = None
    dimming: Optional[DimmingGetBrightness] = None
    color: Optional[ColorGetXY] = None
    color_temperature: Optional[ColorTemperatureGetMirek] = None
    gradient: Optional[ActionActionGradientGet] = None
    effects: Optional[ActionActionEffectsGet] = None
    dynamics: Optional[ActionActionDynamicsGet] = None


@dataclass
class ActionGet:
    target: ActionTargetGet
    action: ActionActionGet


@dataclass
class MetadataImageGet:
    rid: str
    rtype: str


@dataclass
class MetadataGet:
    name: str
    image: Optional[MetadataImageGet] = None


@dataclass
class GroupGet:
    rid: str
    rtype: str


@dataclass
class ColorPaletteGet:
    color: ColorGetXY
    dimming: DimmingGetBrightness


@dataclass
class ColorTemperaturePaletteGet:
    color_temperature: ColorTemperatureGetMirek
    dimming: DimmingGetBrightness


@dataclass
class PaletteGet:
    color: list[ColorPaletteGet]
    dimming: list[DimmingGetBrightness]
    color_temperature: list[ColorTemperaturePaletteGet]


@dataclass
class SceneGet:
    type: Literal["scene"]
    id: str
    actions: list[ActionGet]
    metadata: MetadataGet
    group: GroupGet
    palette: Optional[PaletteGet]
    speed: float
    auto_dynamic: bool
    id_v1: Optional[str] = None


# -------------------------------- ScenePut --------------------------------


@dataclass
class TargetPut:
    rid: Optional[str] = None
    rtype: Optional[str] = None


@dataclass
class DynamicsPutDuration:
    duration: Optional[int] = None


@dataclass
class ActionActionPut:
    on: Optional[OnPut] = None
    dimming: Optional[DimmingPut] = None
    color: Optional[ColorPut] = None
    color_temperature: Optional[ColorTemperaturePut] = None
    gradient: Optional[GradientPut] = None
    effects: Optional[EffectsPut] = None
    dynamics: Optional[DynamicsPutDuration] = None


@dataclass
class ActionPut:
    target: TargetPut
    action: ActionActionPut


@dataclass
class Recall:
    action: Optional[Literal["active", "dynamic_palette", "static"]] = None
    status: Optional[Literal["active", "dynamic_palette"]] = None
    duration: Optional[int] = None
    dimming: Optional[DimmingPut] = None


@dataclass
class MetadataPutName:
    name: str


@dataclass
class ColorPalettePut:
    color: ColorPut
    dimming: DimmingPut


@dataclass
class ColorTemperaturePalettePut:
    color_temperature: ColorTemperaturePut
    dimming: DimmingPut


@dataclass
class PalettePut:
    color: list[ColorPut]
    dimming: list[DimmingPut]
    color_temperature: list[ColorTemperaturePalettePut]


@dataclass
class ScenePut:
    type: Optional[Literal["scene"]] = None
    action: Optional[list[ActionPut]] = None
    recall: Optional[Recall] = None
    metadata: Optional[MetadataPutName] = None
    palette: Optional[PalettePut] = None
    speed: Optional[float] = None
    auto_dynamic: Optional[bool] = None


# -------------------------------- ScenePost --------------------------------


@dataclass
class TargetPost:
    rid: Optional[str] = None
    rtype: Optional[str] = None


@dataclass
class OnPost:
    on: bool


@dataclass
class DimmingPost:
    brightness: float


@dataclass
class XYPost:
    x: float
    y: float


@dataclass
class ColorPost:
    xy: XYPost


@dataclass
class ColorTemperaturePost:
    mirek: int


@dataclass
class GradientPointPost:
    color: ColorPost


@dataclass
class GradientPost:
    points: list[GradientPointPost]
    mode: Optional[
        Literal[
            "interpolated_palette", "interpolated_palette_mirrored", "random_pixelated"
        ]
    ] = None


@dataclass
class EffectsPost:
    effect: Optional[Literal["sparkle", "fire", "no_effect"]] = None


@dataclass
class DynamicsPost:
    duration: Optional[int] = None


@dataclass
class ActionPost:
    on: Optional[OnPost] = None
    dimming: Optional[DimmingPost] = None
    color: Optional[ColorPost] = None
    color_temperature: Optional[ColorTemperaturePost] = None
    gradient: Optional[GradientPost] = None
    effects: Optional[EffectsPost] = None
    dynamics: Optional[DynamicsPost] = None


@dataclass
class ActionPost:
    target: TargetPost
    action: ActionPost


@dataclass
class ImagePost:
    rid: Optional[str] = None
    rtype: Optional[str] = None


@dataclass
class MetadataPost:
    name: str
    image: Optional[ImagePost] = None


@dataclass
class SceneGroupPost:
    rid: Optional[str] = None
    rtype: Optional[str] = None


@dataclass
class ColorPalettePost:
    color: ColorPost
    dimming: DimmingPost


@dataclass
class ColorTemperaturePalettePost:
    color_temperature: ColorTemperaturePost
    dimming: DimmingPost


@dataclass
class PalettePost:
    color: list[ColorPalettePost]
    dimming: list[DimmingPost]
    color_temperature: list[ColorTemperaturePalettePost]


@dataclass
class ScenePost:
    actions: list[ActionPost]
    metadata: MetadataPost
    group: SceneGroupPost
    type: Literal["scene"] = "scene"
    palette: Optional[PalettePost] = None
    speed: Optional[float] = None
    auto_dynamic: Optional[bool] = None


# -------------------------------- RoomGet --------------------------------
@dataclass
class ResourceIdentifierGet:
    rid: str
    rtype: str


@dataclass
class RoomMetadataGet:
    name: str
    archetype: str


@dataclass
class RoomGet:
    type: Literal["room"]
    id: str
    children: list[ResourceIdentifierGet]
    services: list[ResourceIdentifierGet]
    metadata: RoomMetadataGet
    id_v1: Optional[str] = None


# -------------------------------- RoomPut --------------------------------
@dataclass
class ResourceIdentifierPut:
    rid: Optional[str] = None
    rtype: Optional[str] = None


@dataclass
class RoomMetadataPut:
    name: Optional[str] = None
    archetype: Optional[str] = None


@dataclass
class RoomPut:
    type: Optional[Literal["room"]] = None
    children: Optional[list[ResourceIdentifierPut]] = None
    metadata: Optional[RoomMetadataPut] = None


# -------------------------------- RoomPost --------------------------------


@dataclass
class ResourceIdentifierPost:
    rid: Optional[str] = None
    rtype: Optional[str] = None


@dataclass
class RoomMetadataPost:
    name: Optional[str] = None
    archetype: Optional[str] = None


@dataclass
class RoomPost:
    children: list[ResourceIdentifierPost]
    metadata: RoomMetadataPost
    type: Literal["room"] = "room"


# -------------------------------- GroupedLightGet --------------------------------


@dataclass
class GroupedLightGet:
    type: Literal["grouped_light"]
    id: str
    owner: OwnerGet
    id_v1: Optional[str] = None
    on: Optional[OnGet] = None
    dimming: Optional[DimmingGetBrightness] = None
    alert: Optional[AlertGet] = None


# -------------------------------- GroupedLightPut --------------------------------


@dataclass
class GroupedLightPut:
    type: Optional[Literal["grouped_light"]] = None
    on: Optional[OnPut] = None
    dimming: Optional[DimmingPut] = None
    dimming_delta: Optional[DimmingDeltaPut] = None
    color_temperature: Optional[ColorTemperaturePut] = None
    color_temperature_delta: Optional[ColorTemperatureDeltaPut] = None
    color: Optional[ColorPut] = None
    alert: Optional[AlertPut] = None
    dynamics: Optional[DynamicsPutDuration] = None

class HueBridgeButtonNotPressedError(Exception):
    """Raised during authentication when a Hue Bridge's button needs to be
    pressed"""


class HueBridgesDiscoveryError(Exception):
    """Raised when the discovery of Hue bridges fails"""

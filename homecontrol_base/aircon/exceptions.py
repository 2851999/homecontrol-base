class ACAuthenticationError(Exception):
    """Error caused by failing to authenticate with a device"""


class ACInvalidStateError(Exception):
    """Error caused by attempting to assign an invalid ACDeviceState"""

class DeviceConnectionError(Exception):
    """Error to be raised when there is a problem connecting to a device"""


class DeviceNotFoundError(Exception):
    """Error to be raised when a given device isn't found"""

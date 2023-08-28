class ActionNotFoundError(Exception):
    """Raised when attempting to get an action that doesn't exist"""


class RecordTimeout(Exception):
    """Raised after failing to record an action due to a timeout"""


class IncompatibleDeviceError(Exception):
    """Raised when trying to do something with a device that's incompatible"""

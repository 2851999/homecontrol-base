class DeviceConnectionError(Exception):
    """Error to be raised when there is a problem connecting to a device"""


class DeviceNotFoundError(Exception):
    """Error to be raised when a given device isn't found"""


class DatabaseEntryNotFoundError(Exception):
    """Error to be raised when an entry in the database isn't found
    (DeviceNotFoundError often used for devices instead - this is just more
    generic for non-device entries)
    """


class DatabaseDuplicateEntryFoundError(Exception):
    """Error to be raised when a duplicate entry is attempted to be inserted
    into a database but violates a UNIQUE requirement"""

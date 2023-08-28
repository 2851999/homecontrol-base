class ActionNotFoundError(Exception):
    """Raised when attempting to get an action that doesn't exist"""


class RecordTimeout(Exception):
    """Raised after failing to record an action due to a timeout"""

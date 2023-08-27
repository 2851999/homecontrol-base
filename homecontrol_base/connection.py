from typing import Generic, TypeVar

from requests import Session

TSession = TypeVar("TSession", bound=Session)


class BaseConnection(Generic[TSession]):
    """Handles a session object"""

    _session: TSession

    def __init__(self, session: Session) -> None:
        self._session = session

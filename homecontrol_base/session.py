from requests import Session


class SessionWithBaseURL(Session):
    """Used for handling a requests.session object with a base URL"""

    _base_url: str

    def __init__(self, base_url: str = None, *args, **kwargs):
        """Constructor

        Args
            base_url (str): Base URL to use at the start of all request URLs
        """
        self._base_url = base_url
        super().__init__(*args, **kwargs)

    def request(self, method, url, **kwargs):
        return super().request(method, f"{self._base_url}{url}", **kwargs)

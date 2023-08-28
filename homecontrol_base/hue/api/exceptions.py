from requests import HTTPError, Response
from requests.exceptions import JSONDecodeError


def check_response_for_error(response: Response):
    """Checks for an error and raises an appropriate HTTP exception if found

    Attempts to add specific error information given from the Hue API

    Args:
        response (Response): Response to check for errors

    Raises:
        HTTPError: When an error has occurred
    """
    if response.status_code >= 400:
        # Found an error, try and get error messages
        error_messages = None

        try:
            json_data = response.json()
            if "errors" in json_data:
                error_messages = [error["description"] for error in json_data["errors"]]
        except JSONDecodeError:
            pass

        if error_messages is not None:
            raise HTTPError(
                f"{response.status_code} error for url {response.url}"
                f"Error messages:\n"
                "\n".join(error_messages)
            )
        else:
            response.raise_for_status()

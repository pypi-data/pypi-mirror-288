import os
import time

from aws_lambda_powertools import Logger
import requests

DEFAULT_ORIGIN = os.getenv("DEFAULT_ORIGIN", "https://localhost:5173")
APP_NAME = os.getenv("APP_NAME", "augint-tools")


def _call_api(
    api_key: str, url: str, method: str, json_data: dict = None, params=None, retries=0, retry_delay=500
) -> requests.Response:
    """
    Call the Lead Momentum API using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        url (str): The URL for the API endpoint.
        method (str): The HTTP method to use for the request.
        json_data (dict, optional): The JSON data to include in the request body. Defaults to None.

    Returns:
        requests.Response: The API response containing the requested information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    headers = get_headers(api_key)
    verb = method.lower()
    func = getattr(requests, verb)
    json_data = json_data or {}
    params = params or {}

    for remaining_retries in range(retries + 1)[::-1]:
        try:
            response = func(url=url, headers=headers, json=json_data, params=params)
            response.raise_for_status()
            logger.debug(f"API call successful")
            return response
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            remaining_retries -= 1
            if remaining_retries > 0:
                logger.warning(f"Encountered exception: {e}")
                logger.warning(f"Retrying in {retry_delay} ms.")
                time.sleep(retry_delay / 1000)
                continue
            else:
                logger.error(f"Failure in _call_api, encountered exception: {e}")
                logger.info(f"API call failure with no retries: {e}")
                raise
    raise


def get_logger() -> Logger:
    log_level = os.environ.get("LOG_LEVEL", "INFO")  # Default to INFO if not set
    _logger = Logger(service=f"{APP_NAME}", level=log_level)
    return _logger


def get_headers(api_key: str, origin: str = DEFAULT_ORIGIN) -> dict:
    headers = {
        "Content-Type": "application/json",
        # "Origin": origin,
        "Authorization": f"Bearer {api_key}",
    }
    return headers


logger = get_logger()

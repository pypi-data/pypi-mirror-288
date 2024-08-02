import requests

from src.leadmo_api.models.workflow_endpoint_params import GetWorkflowsParams
from src.leadmo_api.util import get_headers, logger, _call_api

LEADMO_API_V1_WORKFLOWS_URL = "https://rest.gohighlevel.com/v1/workflows/"


def get_workflows(api_key: str, params: GetWorkflowsParams = None, retries=3, retry_delay=500) -> requests.Response:
    """
    Retrieve workflows using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetWorkflowsParams, optional): Parameters for retrieving workflows. Defaults to None.

    Returns:
        requests.Response: The API response containing the workflows information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    if not params:
        logger.info("No params provided. Getting all workflows.")

    url = LEADMO_API_V1_WORKFLOWS_URL
    try:
        return _call_api(api_key, url, "GET", retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to get workflows: {e}")
        raise

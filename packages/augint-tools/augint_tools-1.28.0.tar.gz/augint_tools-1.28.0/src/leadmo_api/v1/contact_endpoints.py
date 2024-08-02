import json
import urllib.request

import requests

from src.leadmo_api.models.contact_endpoint_params import (
    CreateContactParams,
    UpdateContactParams,
    LookupContactParams,
    DeleteContactParams,
    GetContactByIdParams,
    GetContactAppointmentsParams,
    TagContactParams,
    RemoveTagFromContactParams,
    AddContactToWorkflowParams,
)
from src.leadmo_api.util import logger, _call_api

# Predefined URL constants
LEADMO_API_V1_CONTACTS_URL = "https://rest.gohighlevel.com/v1/contacts/"
LEADMO_API_V1_LOOKUP_CONTACT_URL = "https://rest.gohighlevel.com/v1/contacts/lookup"


def create_contact(api_key: str, params: CreateContactParams, retries=0, retry_delay=500) -> requests.Response:
    """
    Create a new contact using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (CreateContactParams): Parameters required for creating a contact.

    Returns:
        requests.Response: The API response containing the created contact information.

    Raises:
        ValueError: If neither 'email' nor 'phone' is provided.
        requests.exceptions.RequestException: If the request fails.
    """
    contact_data_json = params.model_dump_json(by_alias=True, exclude_none=True)
    json_data = json.loads(contact_data_json)

    try:
        return _call_api(api_key, LEADMO_API_V1_CONTACTS_URL, "POST", json_data, retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.debug(f"Failed to create contact: {e}")
        raise


def lookup_contact(api_key: str, params: LookupContactParams, retries=3, retry_delay=500) -> requests.Response:
    """
    Lookup a contact using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (LookupContactParams): Parameters for looking up a contact.

    Returns:
        requests.Response: The API response containing the contact information.

    Raises:
        ValueError: If neither 'email' nor 'phone' is provided.
        requests.exceptions.RequestException: If the request fails.
    """
    params = params.model_dump(exclude_none=True, by_alias=True)
    params_str = "&".join([f"{k}={urllib.request.pathname2url(v)}" for k, v in params.items()])
    url = f"{LEADMO_API_V1_LOOKUP_CONTACT_URL}?{params_str}"

    try:
        return _call_api(api_key, url, "GET", retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.debug(f"Failed to create contact: {e}")
        raise


def get_contact_by_id(api_key: str, params: GetContactByIdParams, retries=3, retry_delay=500) -> requests.Response:
    """
    Retrieve a contact by its unique identifier.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetContactByIdParams): Parameters containing the contact ID.

    Returns:
        requests.Response: The API response containing the contact information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    url = f"{LEADMO_API_V1_CONTACTS_URL}{params.contact_id}"
    try:
        return _call_api(api_key, url, "GET", retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.debug(f"Failed to create contact: {e}")
        raise


def update_contact(api_key: str, params: UpdateContactParams, retries=2, retry_delay=1000) -> requests.Response:
    """
    Update an existing contact using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (UpdateContactParams): Parameters for updating a contact.

    Returns:
        requests.Response: The API response containing the updated contact information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    if not params.contact_id:
        lookup_contact_response = lookup_contact(
            api_key, LookupContactParams(**params.model_dump(by_alias=True, exclude_none=True))
        )
        first_contact = lookup_contact_response.json().get("contacts")[0]
        params.contact_id = first_contact.get("id")

    contact_data_json = params.model_dump_json(by_alias=True, exclude_none=True)
    json_data = json.loads(contact_data_json)
    contact_id = json_data.pop("contactId")
    url = f"{LEADMO_API_V1_CONTACTS_URL}{contact_id}"

    try:
        logger.info(f"Updating contact: {url=}, {json_data=}")
        return _call_api(api_key, url, "PUT", json_data, retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.debug(f"Failed to create contact: {e}")
        raise


def delete_contact(api_key: str, params: DeleteContactParams, retries=0, retry_delay=500) -> requests.Response:
    """
    Delete a contact by its unique identifier.

    Args:
        api_key (str): The API key for authenticating requests.
        params (DeleteContactParams): Parameters containing the contact ID.

    Returns:
        requests.Response: The API response confirming the contact deletion.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    if not params.contact_id:
        lookup_contact_response = lookup_contact(
            api_key, LookupContactParams(**params.model_dump(by_alias=True, exclude_none=True))
        )
        first_contact = lookup_contact_response.json().get("contacts")[0]
        params.contact_id = first_contact.get("id")

    url = f"{LEADMO_API_V1_CONTACTS_URL}{params.contact_id}"
    try:
        return _call_api(api_key, url, "DELETE", retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.debug(f"Failed to create contact: {e}")
        raise


def get_contact_appointments(api_key: str, params: GetContactAppointmentsParams, retries=3, retry_delay=500) -> requests.Response:
    """
    Retrieve appointments associated with a specific contact.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetContactAppointmentsParams): Parameters containing the contact ID.

    Returns:
        requests.Response: The API response containing the contact appointments information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    url = f"{LEADMO_API_V1_CONTACTS_URL}{params.contact_id}/appointments"
    try:
        return _call_api(api_key, url, "GET", retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.debug(f"Failed to create contact: {e}")
        raise


def tag_contact(api_key: str, params: TagContactParams, retries=0, retry_delay=500) -> requests.Response:
    """
    Add tags to a specific contact.

    Args:
        api_key (str): The API key for authenticating requests.
        params (TagContactParams): Parameters for adding tags to a contact.

    Returns:
        requests.Response: The API response confirming the addition of tags.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    params_dict = params.model_dump(exclude_none=True, by_alias=True)
    contact_id = params_dict.pop("contactId")
    url = f"{LEADMO_API_V1_CONTACTS_URL}{contact_id}/tags"

    try:
        return _call_api(api_key, url, "POST", json_data=params_dict, retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.debug(f"Failed to create contact: {e}")
        raise


def remove_tag_from_contact(api_key: str, params: RemoveTagFromContactParams, retries=0, retry_delay=500) -> requests.Response:
    """
    Remove tags from a specific contact.

    Args:
        api_key (str): The API key for authenticating requests.
        params (RemoveTagFromContactParams): Parameters for removing tags from a contact.

    Returns:
        requests.Response: The API response confirming the removal of tags.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    params_dict = params.model_dump(exclude_none=True, by_alias=True)
    contact_id = params_dict.pop("contactId")
    url = f"{LEADMO_API_V1_CONTACTS_URL}{contact_id}/tags"

    try:
        return _call_api(api_key, url, "DELETE", json_data=params_dict, retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.debug(f"Failed to create contact: {e}")
        raise


def add_contact_to_workflow(api_key: str, params: AddContactToWorkflowParams, retries=0, retry_delay=500) -> requests.Response:
    """
    Add a contact to a workflow.

    Args:
        api_key (str): The API key for authenticating requests.
        params (AddContactToWorkflowParams): Parameters for adding a contact to a workflow.

    Returns:
        requests.Response: The API response confirming the addition to the workflow.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    url = f"{LEADMO_API_V1_CONTACTS_URL}{params.contact_id}/workflow/{params.workflow_id}"

    try:
        return _call_api(api_key, url, "POST", retries=retries, retry_delay=retry_delay)
    except Exception as e:
        logger.debug(f"Failed to create contact: {e}")
        raise

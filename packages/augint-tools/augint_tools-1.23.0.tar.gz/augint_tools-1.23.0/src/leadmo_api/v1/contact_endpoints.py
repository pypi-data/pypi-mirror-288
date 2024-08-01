import json

import requests
from src.leadmo_api.util import get_headers, logger
from src.leadmo_api.models.contact import CreateContact, UpdateContact, LookupContact, DeleteContact, GetContactById

# Predefined URL constants
LEADMO_API_V1_CONTACTS_URL = "https://rest.gohighlevel.com/v1/contacts/"
LEADMO_API_V1_LOOKUP_CONTACT_URL = "https://rest.gohighlevel.com/v1/contacts/lookup"


def create_contact(api_key: str, create_contact: CreateContact) -> requests.Response:
    """
    Create a contact in Lead Momentum.

    :param api_key: The API key for authenticating the request.
    :param create_contact: CreateContactModel instance containing contact details.
    :return: The response from the Lead Momentum API.
    """
    logger.debug(f"Creating a new contact {create_contact}")
    if not create_contact.email and not create_contact.phone:
        raise ValueError("Either 'email' or 'phone' must be provided to create a contact.")

    contact_data_json = create_contact.model_dump_json(by_alias=True, exclude_none=True)
    json_data = json.loads(contact_data_json)
    headers = get_headers(api_key)

    try:
        response = requests.post(url=LEADMO_API_V1_CONTACTS_URL, headers=headers, json=json_data)
        response.raise_for_status()
        logger.debug("Successfully created a contact")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create contact: {e}")
        raise


def lookup_contact(api_key: str, lookup_contact: LookupContact) -> requests.Response:
    """
    Lookup a contact in Lead Momentum by email or phone.

    :param api_key: The API key for authenticating the request.
    :param lookup_contact: LookupContactModel instance containing lookup details.
    :return: The response from the Lead Momentum API.
    """
    lookup_data_dict = lookup_contact.model_dump(exclude_none=True, by_alias=True)

    if not lookup_data_dict:
        raise ValueError("Either 'email' or 'phone' must be provided to lookup a contact.")

    headers = get_headers(api_key)

    logger.info("Looking up contact with parameters", extra=lookup_data_dict)

    try:
        response = requests.get(url=LEADMO_API_V1_LOOKUP_CONTACT_URL, headers=headers, params=lookup_data_dict)
        response.raise_for_status()
        logger.info("Successfully looked up contact")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to lookup contact: {e}")
        raise


def get_contact_by_id(api_key: str, get_contact_by_id: GetContactById) -> requests.Response:
    """
    Get an contact by ID from Lead Momentum.
    @param api_key: The API key for authenticating the request.
    @param appointment_id: The ID of the contact to retrieve.
    @return: The response from the Lead Momentum API.
    """

    url = f"{LEADMO_API_V1_CONTACTS_URL}{get_contact_by_id.contact_id}"

    headers = get_headers(api_key)

    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get appointment by ID: {e}")
        raise


def update_contact(api_key: str, update_contact: UpdateContact) -> requests.Response:
    """
    Update a contact in Lead Momentum.
    :param api_key: The API key for authenticating the request.
    :param update_contact: The UpdateContactModel instance containing the contact details.
    :return:
    """
    if not update_contact.contact_id:
        lookup_contact_response = lookup_contact(
            api_key, LookupContact(**update_contact.model_dump(by_alias=True, exclude_none=True))
        )
        first_contact = lookup_contact_response.json().get("contacts")[0]
        update_contact.contact_id = first_contact.get("id")

    contact_data_json = update_contact.model_dump_json(by_alias=True, exclude_none=True)
    json_data = json.loads(contact_data_json)

    headers = get_headers(api_key)

    url = f"{LEADMO_API_V1_CONTACTS_URL}{update_contact.contact_id}"
    try:
        response = requests.put(url=url, headers=headers, json=json_data)
        response.raise_for_status()
        logger.info("Successfully updated contact")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to update contact: {e}")
        raise


def delete_contact(api_key: str, delete_contact: DeleteContact) -> requests.Response:
    """
    Delete a contact by ID from Lead Momentum.

    :param api_key: The API key for authenticating the request.
    :param contact_data: DeleteContactModel instance containing the contact ID.
    :return: The response from the Lead Momentum API.
    """
    if not delete_contact.contact_id:
        lookup_contact_response = lookup_contact(
            api_key, LookupContact(**delete_contact.model_dump(by_alias=True, exclude_none=True))
        )
        first_contact = lookup_contact_response.json().get("contacts")[0]
        delete_contact.contact_id = first_contact.get("id")

    url = f"{LEADMO_API_V1_CONTACTS_URL}{delete_contact.contact_id}"
    headers = get_headers(api_key)

    logger.info(f"Deleting contact by ID: {delete_contact.contact_id}")

    try:
        response = requests.delete(url=url, headers=headers)
        response.raise_for_status()
        logger.info("Successfully deleted contact")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to delete contact: {e}")
        raise

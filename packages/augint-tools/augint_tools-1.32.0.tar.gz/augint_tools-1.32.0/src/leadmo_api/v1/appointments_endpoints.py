import json
import requests

from src.leadmo_api.models.appointment_endpoint_params import (
    GetAppointmentSlotsParams,
    CreateAppointmentParams,
    GetAppointmentByIdParams,
    GetAppointmentsParams,
    DeleteAppointmentParams,
    UpdateAppointmentParams,
    UpdateAppointmentStatusParams,
)
from src.leadmo_api.util import get_headers, logger, _call_api

LEADMO_API_V1_APPOINTMENTS_URL = "https://rest.gohighlevel.com/v1/appointments/"
LEADMO_API_V1_GET_APPOINTMENT_SLOTS_URL = "https://rest.gohighlevel.com/v1/appointments/slots/"


def get_available_appointment_slots(
    api_key: str, params: GetAppointmentSlotsParams, retries=3, retry_delay=500
) -> requests.Response:
    """
    Retrieve available appointment slots using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetAppointmentSlotsParams): Parameters for retrieving appointment slots.

    Returns:
        requests.Response: The API response containing available appointment slots.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    get_appointment_slots_dict = params.model_dump(exclude_none=True, by_alias=True)
    url = LEADMO_API_V1_GET_APPOINTMENT_SLOTS_URL
    try:
        return _call_api(api_key, url, "GET", params=get_appointment_slots_dict, retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to get available appointment slots: {e}")
        raise


def create_appointment(api_key: str, params: CreateAppointmentParams, retries=0, retry_delay=500) -> requests.Response:
    """
    Create a new appointment using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (CreateAppointmentParams): Parameters required for creating an appointment.

    Returns:
        requests.Response: The API response containing the created appointment information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    contact_data_json = params.model_dump_json(by_alias=True, exclude_none=True)
    json_data = json.loads(contact_data_json)
    url = LEADMO_API_V1_APPOINTMENTS_URL
    try:
        return _call_api(api_key, url, "POST", json_data=json_data, retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to create appointment: {e}")
        raise


def get_appointment_by_id(api_key: str, params: GetAppointmentByIdParams, retries=3, retry_delay=500) -> requests.Response:
    """
    Retrieve an appointment by its unique identifier.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetAppointmentByIdParams): Parameters containing the appointment ID.

    Returns:
        requests.Response: The API response containing the appointment information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{params.appointment_id}"

    try:
        return _call_api(api_key, url, "GET", retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to get appointment by id: {e}")
        raise


def get_appointments(api_key: str, params: GetAppointmentsParams, retries=3, retry_delay=500) -> requests.Response:
    """
    Retrieve appointments based on the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (GetAppointmentsParams): Parameters for retrieving appointments.

    Returns:
        requests.Response: The API response containing the appointments information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    get_appointments_dict = params.model_dump(exclude_none=True, by_alias=True)
    url = LEADMO_API_V1_APPOINTMENTS_URL
    try:
        return _call_api(api_key, url, "GET", params=get_appointments_dict, retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to get appointments: {e}")
        raise


def delete_appointment(api_key: str, params: DeleteAppointmentParams, retries=0, retry_delay=500) -> requests.Response:
    """
    Delete an appointment by its unique identifier.

    Args:
        api_key (str): The API key for authenticating requests.
        params (DeleteAppointmentParams): Parameters containing the appointment ID.

    Returns:
        requests.Response: The API response confirming the appointment deletion.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{params.appointment_id}"

    try:
        return _call_api(api_key, url, "DELETE", retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to delete appointment: {e}")
        raise


def update_appointment(api_key: str, params: UpdateAppointmentParams, retries=0, retry_delay=500) -> requests.Response:
    """
    Update an existing appointment using the provided parameters.

    Args:
        api_key (str): The API key for authenticating requests.
        params (UpdateAppointmentParams): Parameters for updating an appointment.

    Returns:
        requests.Response: The API response containing the updated appointment information.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    appointment_data = params.model_dump(by_alias=True, exclude_none=True)
    appointment_id = appointment_data.pop("appointmentId")
    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{appointment_id}"

    try:
        return _call_api(api_key, url, "PUT", json_data=appointment_data, retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to update appointment: {e}")
        raise


def update_appointment_status(
    api_key: str, params: UpdateAppointmentStatusParams, retries=0, retry_delay=500
) -> requests.Response:
    """
    Update the status of an appointment.

    Args:
        api_key (str): The API key for authenticating requests.
        params (UpdateAppointmentStatusParams): Parameters for updating the appointment status.

    Returns:
        requests.Response: The API response confirming the status update.

    Raises:
        requests.exceptions.RequestException: If the request fails.
    """
    appointment_data = params.model_dump(by_alias=True, exclude_none=True)
    appointment_id = appointment_data.pop("appointmentId")
    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{appointment_id}/status"

    try:
        return _call_api(api_key, url, "PUT", json_data=appointment_data, retries=retries, retry_delay=retry_delay)
    except requests.exceptions.RequestException as e:
        logger.debug(f"Failed to update appointment status: {e}")
        raise

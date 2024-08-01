import json

import requests

from src.leadmo_api.models.appointments import (
    GetAppointmentSlots,
    CreateAppointment,
    GetAppointmentById,
    GetAppointments,
    DeleteAppointment,
    UpdateAppointment,
    UpdateAppointmentStatus,
)
from src.leadmo_api.util import get_headers, logger

LEADMO_API_V1_APPOINTMENTS_URL = "https://rest.gohighlevel.com/v1/appointments/"
LEADMO_API_V1_GET_APPOINTMENT_SLOTS_URL = "https://rest.gohighlevel.com/v1/appointments/slots/"


def get_available_appointment_slots(api_key: str, get_appointment_slots: GetAppointmentSlots) -> requests.Response:
    """
    Get available appointment slots from Lead Momentum.
    :param api_key: The API key for authenticating the request.
    :param get_appointment_slots: The GetAppointmentSlots model instance containing the query parameters.
    :return: The response from the Lead Momentum API.
    """
    get_appointment_slots_dict = get_appointment_slots.model_dump(exclude_none=True, by_alias=True)

    headers = get_headers(api_key)
    logger.info("Getting available appointment slots with parameters")

    try:
        response = requests.get(url=LEADMO_API_V1_GET_APPOINTMENT_SLOTS_URL, headers=headers, params=get_appointment_slots_dict)
        response.raise_for_status()
        logger.info("Successfully retrieved available appointment slots")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get available appointment slots: {e}")
        raise


def create_appointment(api_key: str, create_appointment: CreateAppointment) -> requests.Response:
    """
    Create an appointment in Lead Momentum. If the contact does not exist, it will be created.
    @param api_key: The API key for authenticating the request.
    @param create_appointment: The CreateAppointment model instance containing the appointment details.
    @return: The response from the Lead Momentum API.
    """

    logger.debug(f"Creating a new appointment {create_appointment}")
    contact_data_json = create_appointment.model_dump_json(by_alias=True, exclude_none=True)
    json_data = json.loads(contact_data_json)
    headers = get_headers(api_key)

    try:
        response = requests.post(url=LEADMO_API_V1_APPOINTMENTS_URL, headers=headers, json=json_data)
        response.raise_for_status()
        logger.debug("Successfully created a appointment")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create appointment: {e}")
        raise


def get_appointment_by_id(api_key: str, get_appointment_by_id: GetAppointmentById) -> requests.Response:
    """
    Get an appointment by ID from Lead Momentum.
    @param api_key: The API key for authenticating the request.
    @param appointment_id: The ID of the appointment to retrieve.
    @return: The response from the Lead Momentum API.
    """

    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{get_appointment_by_id.appointment_id}"

    headers = get_headers(api_key)

    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get appointment by ID: {e}")
        raise


def get_appointments(api_key: str, get_appointments: GetAppointments) -> requests.Response:
    """
    Get all appointments from Lead Momentum.
    @param api_key: The API key for authenticating the request.
    @param get_appointments: The GetAppointments model instance containing the query parameters.
    @return: The response from the Lead Momentum API.
    """
    get_appointments_dict = get_appointments.model_dump(exclude_none=True, by_alias=True)

    headers = get_headers(api_key)
    logger.info("Getting all appointments with parameters")

    try:
        response = requests.get(url=LEADMO_API_V1_APPOINTMENTS_URL, headers=headers, params=get_appointments_dict)
        response.raise_for_status()
        logger.info("Successfully retrieved all appointments")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get all appointments: {e}")
        raise


def delete_appointment(api_key: str, delete_appointment_params: DeleteAppointment) -> requests.Response:
    """
    Delete an appointment by ID from Lead Momentum.
    @param api_key: The API key for authenticating the request.
    @param appointment_id: The ID of the appointment to delete.
    @return: The response from the Lead Momentum API.
    """

    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{delete_appointment_params.appointment_id}"

    headers = get_headers(api_key)

    try:
        response = requests.delete(url=url, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get appointment by ID: {e}")
        raise


def update_appointment(api_key: str, update_appointment: UpdateAppointment) -> requests.Response:
    """
    Update an appointment in Lead Momentum.
    :param api_key: The API key for authenticating the request.
    :param update_appointment: The UpdateAppointment model instance containing the appointment details.
    :return: The response from the Lead Momentum API.
    """

    logger.debug(f"Updating a new appointment {create_appointment}")
    appointment_data = update_appointment.model_dump(by_alias=True, exclude_none=True)
    appointment_id = appointment_data.pop("appointmentId")
    headers = get_headers(api_key)
    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{appointment_id}"

    try:
        response = requests.put(url=url, headers=headers, json=appointment_data)
        response.raise_for_status()
        logger.debug("Successfully updated appointment")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to update appointment: {e}")
        raise


def update_appointment_status(api_key: str, update_appointment_status: UpdateAppointmentStatus) -> requests.Response:
    """
    Update an appointment in Lead Momentum.
    :param api_key: The API key for authenticating the request.
    :param update_appointment: The UpdateAppointment model instance containing the appointment details.
    :return: The response from the Lead Momentum API.
    """
    logger.debug(f"Updating a new appointment {create_appointment}")
    appointment_data = update_appointment_status.model_dump(by_alias=True, exclude_none=True)
    appointment_id = appointment_data.pop("appointmentId")
    headers = get_headers(api_key)
    url = f"{LEADMO_API_V1_APPOINTMENTS_URL}{appointment_id}/status"

    try:
        response = requests.put(url=url, headers=headers, json=appointment_data)
        response.raise_for_status()
        logger.debug("Successfully updated appointment")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to update appointment: {e}")
        raise

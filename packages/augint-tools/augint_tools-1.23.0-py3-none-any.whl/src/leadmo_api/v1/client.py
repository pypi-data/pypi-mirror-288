import os
from src.util import logger
from src.leadmo_api.models.appointments import (
    GetAppointmentSlots,
    CreateAppointment,
    GetAppointmentById,
    GetAppointments,
    DeleteAppointment,
    UpdateAppointment,
    UpdateAppointmentStatus,
)
from src.leadmo_api.models.contact import CreateContact, LookupContact, GetContactById, UpdateContact, DeleteContact
from src.leadmo_api.v1.appointments_endpoints import (
    get_available_appointment_slots,
    create_appointment,
    get_appointment_by_id,
    get_appointments,
    delete_appointment,
    update_appointment,
    update_appointment_status,
)
from src.leadmo_api.v1.contact_endpoints import create_contact, lookup_contact, get_contact_by_id, update_contact, delete_contact


class LeadmoApiV1:
    def __init__(self, api_key: str = os.getenv("LEADMO_BEARER_TOKEN")):
        self.api_key = api_key

    def create_contact(self, **kwargs):
        try:
            create_contact_params = CreateContact(**kwargs)
            response = create_contact(api_key=self.api_key, create_contact=create_contact_params)
            return response.json()
        except Exception as e:
            logger.debug("Failed to create contact.")
            raise

    def lookup_contact(self, **kwargs):
        try:
            lookup_contact_params = LookupContact(**kwargs)
            response = lookup_contact(api_key=self.api_key, lookup_contact=lookup_contact_params)
            return response.json()
        except Exception as e:
            logger.debug("Failed to lookup contact.")
            raise

    def get_contact_by_id(self, contact_id: str):
        try:
            get_contact_by_id_params = GetContactById(contact_id=contact_id)
            response = get_contact_by_id(api_key=self.api_key, get_contact_by_id=get_contact_by_id_params)
            return response.json()
        except Exception as e:
            logger.debug("Failed to get contact by id.")
            raise

    def update_contact(self, **kwargs):
        try:
            update_contact_params = UpdateContact(**kwargs)
            response = update_contact(api_key=self.api_key, update_contact=update_contact_params)
            return response.json()
        except Exception as e:
            logger.debug("Failed to update contact.")
            raise

    def delete_contact(self, **kwargs):
        try:
            delete_contact_params = DeleteContact(**kwargs)
            delete_contact(api_key=self.api_key, delete_contact=delete_contact_params)
        except Exception as e:
            logger.debug("Failed to delete contact.")
            raise

    def get_available_appointment_slots(self, **kwargs):
        try:
            get_appointment_slots = GetAppointmentSlots(**kwargs)
            response = get_available_appointment_slots(api_key=self.api_key, get_appointment_slots=get_appointment_slots)
            return response.json()
        except Exception as e:
            logger.debug("Failed to get available appointment slots.")
            raise

    def create_appointment(self, **kwargs):
        try:
            create_appointment_params = CreateAppointment(**kwargs)
            response = create_appointment(api_key=self.api_key, create_appointment=create_appointment_params)
            return response.json()
        except Exception as e:
            logger.debug("Failed to create appointment.")
            raise

    def get_appointment_by_id(self, appointment_id: str):
        try:
            get_appointment_by_id_params = GetAppointmentById(appointment_id=appointment_id)
            response = get_appointment_by_id(api_key=self.api_key, get_appointment_by_id=get_appointment_by_id_params)
            return response.json()
        except Exception as e:
            logger.debug("Failed to get appointment by id.")
            raise

    def get_appointments(self, **kwargs):
        try:
            get_appointments_params = GetAppointments(**kwargs)
            response = get_appointments(api_key=self.api_key, get_appointments=get_appointments_params)
            return response.json()
        except Exception as e:
            logger.debug("Failed to get appointments.")
            raise

    def delete_appointment(self, **kwargs):
        try:
            delete_appointment_params = DeleteAppointment(**kwargs)
            delete_appointment(api_key=self.api_key, delete_appointment_params=delete_appointment_params)
        except Exception as e:
            logger.debug("Failed to delete appointment.")
            raise

    def update_appointment(self, **kwargs):
        try:
            update_appointment_params = UpdateAppointment(**kwargs)
            response = update_appointment(api_key=self.api_key, update_appointment=update_appointment_params)
            return response.json()
        except Exception as e:
            logger.debug("Failed to update appointment.")
            raise

    def update_appointment_status(self, **kwargs):
        try:
            update_appointment_status_params = UpdateAppointmentStatus(**kwargs)
            response = update_appointment_status(api_key=self.api_key, update_appointment_status=update_appointment_status_params)
            return response.json()
        except Exception as e:
            logger.debug("Failed to update appointment status.")
            raise

import inspect
import os
from typing import Type, Callable
import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.leadmo_api.models.workflow_endpoint_params import GetWorkflowsParams
from src.leadmo_api.v1.workflow_endpoints import get_workflows
from src.util import logger
from src.leadmo_api.models.appointment_endpoint_params import (
    GetAppointmentSlotsParams,
    CreateAppointmentParams,
    GetAppointmentByIdParams,
    GetAppointmentsParams,
    DeleteAppointmentParams,
    UpdateAppointmentParams,
    UpdateAppointmentStatusParams,
)
from src.leadmo_api.models.contact_endpoint_params import (
    CreateContactParams,
    LookupContactParams,
    GetContactByIdParams,
    UpdateContactParams,
    DeleteContactParams,
    GetContactAppointmentsParams,
    TagContactParams,
    RemoveTagFromContactParams,
    AddContactToWorkflowParams,
)
from src.leadmo_api.v1.appointments_endpoints import (
    get_available_appointment_slots,
    create_appointment,
    get_appointment_by_id,
    get_appointments,
    delete_appointment,
    update_appointment,
    update_appointment_status,
)
from src.leadmo_api.v1.contact_endpoints import (
    create_contact,
    lookup_contact,
    get_contact_by_id,
    update_contact,
    delete_contact,
    get_contact_appointments,
    tag_contact,
    remove_tag_from_contact,
    add_contact_to_workflow,
)


def type_hint_from_params(param_class: Type):
    """
    A decorator that assigns type hints to the wrapped function based on the provided parameter class.

    Args:
        param_class (Type): The parameter class containing the type annotations.

    Returns:
        Callable: The decorated function with updated type hints.
    """

    def decorator(func: Callable) -> Callable:
        # Create a dictionary of parameter names and their types
        param_types = {k: v for k, v in param_class.__annotations__.items()}

        # Generate a signature with the appropriate type hints
        new_signature = inspect.signature(func).replace(
            parameters=[inspect.Parameter(name="kwargs", kind=inspect.Parameter.VAR_KEYWORD, annotation=param_types)]
        )
        func.__signature__ = new_signature
        return func

    return decorator


class LeadmoApiV1:
    """
    A class for interacting with the Lead Momentum API.

    This class provides methods to create, update, delete, and retrieve contacts and appointments
    using the Lead Momentum API. It uses an API key for authentication.
    """

    def __init__(self, api_key: str = os.getenv("LEADMO_BEARER_TOKEN")):
        """
        Initialize the LeadmoApiV1 class with the provided API key.

        Args:
            api_key (str): The API key for authenticating requests. Defaults to the LEADMO_BEARER_TOKEN
                           environment variable if not provided.
        """
        self.api_key = api_key
        self.executor = ThreadPoolExecutor()

    #######################################
    # Contact Endpoints
    #######################################

    @type_hint_from_params(CreateContactParams)
    def create_contact(self, retries=0, retry_delay=500, **kwargs):
        """
        Create a new contact using the provided parameters.

        Args:
            **kwargs: Parameters required for creating a contact. Refer to CreateContactParams for details.

        Returns:
            dict: The API response containing the created contact information.

        Raises:
            Exception: If the contact creation fails.
        """
        try:
            create_contact_params = CreateContactParams(**kwargs)
            response = create_contact(
                api_key=self.api_key, params=create_contact_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to create contact: {e}")
            raise

    @type_hint_from_params(LookupContactParams)
    def lookup_contact(self, retries=0, retry_delay=500, **kwargs):
        """
        Lookup a contact using the provided parameters.

        Args:
            **kwargs: Parameters for looking up a contact. Refer to LookupContactParams for details.

        Returns:
            dict: The API response containing the contact information.

        Raises:
            Exception: If the contact lookup fails.
        """
        try:
            lookup_contact_params = LookupContactParams(**kwargs)
            response = lookup_contact(
                api_key=self.api_key, params=lookup_contact_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to lookup contact: {e}")
            raise

    @type_hint_from_params(GetContactByIdParams)
    def get_contact_by_id(self, retries=3, retry_delay=500, **kwargs):
        """
        Retrieve a contact by its unique identifier.

        Args:
            contact_id (str): The unique identifier of the contact.

        Returns:
            dict: The API response containing the contact information.

        Raises:
            Exception: If the contact retrieval fails.
        """
        try:
            get_contact_by_id_params = GetContactByIdParams(**kwargs)
            response = get_contact_by_id(
                api_key=self.api_key, params=get_contact_by_id_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to get contact by id: {e}")
            raise

    @type_hint_from_params(UpdateContactParams)
    def update_contact(self, retries=2, retry_delay=1000, **kwargs):
        """
        Update an existing contact using the provided parameters.

        Args:
            **kwargs: Parameters for updating a contact. Refer to UpdateContactParams for details.

        Returns:
            dict: The API response containing the updated contact information.

        Raises:
            Exception: If the contact update fails.
        """
        try:
            update_contact_params = UpdateContactParams(**kwargs)
            response = update_contact(
                api_key=self.api_key, params=update_contact_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to update contact: {e}")
            raise

    @type_hint_from_params(DeleteContactParams)
    def delete_contact(self, retries=0, retry_delay=500, **kwargs):
        """
        Delete a contact using the provided parameters.

        Args:
            **kwargs: Parameters for deleting a contact. Refer to DeleteContactParams for details.

        Raises:
            Exception: If the contact deletion fails.
        """
        try:
            delete_contact_params = DeleteContactParams(**kwargs)
            response = delete_contact(
                api_key=self.api_key, params=delete_contact_params, retries=retries, retry_delay=retry_delay
            )
            return response
        except Exception as e:
            logger.debug(f"Failed to delete contact: {e}")
            raise

    @type_hint_from_params(GetContactAppointmentsParams)
    def get_contact_appointments(self, retries=3, retry_delay=500, **kwargs):
        """
        Retrieve appointments associated with a specific contact.

        Args:
            **kwargs: Parameters for retrieving contact appointments. Refer to GetContactAppointmentsParams for details.

        Returns:
            dict: The API response containing the contact appointments information.

        Raises:
            Exception: If retrieving contact appointments fails.
        """
        try:
            get_contact_appointments_params = GetContactAppointmentsParams(**kwargs)
            response = get_contact_appointments(
                api_key=self.api_key, params=get_contact_appointments_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to get contact appointments: {e}")
            raise

    @type_hint_from_params(TagContactParams)
    def tag_contact(self, retries=0, retry_delay=500, **kwargs):
        """
        Add tags to a specific contact.

        Args:
            **kwargs: Parameters for adding tags to a contact. Refer to AddContactTagsParams for details.

        Returns:
            dict: The API response confirming the addition of tags.

        Raises:
            Exception: If adding contact tags fails.
        """
        try:
            add_contact_tags_params = TagContactParams(**kwargs)
            response = tag_contact(api_key=self.api_key, params=add_contact_tags_params, retries=retries, retry_delay=retry_delay)
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to add contact tags: {e}")
            raise

    @type_hint_from_params(RemoveTagFromContactParams)
    def remove_tag_from_contact(self, retries=0, retry_delay=500, **kwargs):
        """
        Remove tags from a specific contact.

        Args:
            **kwargs: Parameters for removing tags from a contact. Refer to RemoveContactTagsParams for details.

        Returns:
            dict: The API response confirming the removal of tags.

        Raises:
            Exception: If removing contact tags fails.
        """
        try:
            remove_contact_tags_params = RemoveTagFromContactParams(**kwargs)
            response = remove_tag_from_contact(
                api_key=self.api_key, params=remove_contact_tags_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to remove contact tags: {e}")
            raise

    @type_hint_from_params(AddContactToWorkflowParams)
    def add_contact_to_workflow(self, retries=0, retry_delay=500, **kwargs):
        """
        Add a contact to a workflow.

        Args:
            **kwargs: Parameters for adding a contact to a workflow. Refer to AddContactToWorkflowParams for details.

        Returns:
            dict: The API response confirming the addition of the contact to the workflow.

        Raises:
            Exception: If adding the contact to the workflow fails.
        """
        try:
            add_contact_to_workflow_params = AddContactToWorkflowParams(**kwargs)
            response = add_contact_to_workflow(
                api_key=self.api_key, params=add_contact_to_workflow_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to add contact to workflow: {e}")
            raise

    #######################################
    # Appointment Endpoints
    #######################################

    @type_hint_from_params(GetAppointmentSlotsParams)
    def get_available_appointment_slots(self, retries=3, retry_delay=500, **kwargs):
        """
        Retrieve available appointment slots for a calendar.

        Args:
            **kwargs: Parameters for retrieving appointment slots. Refer to GetAppointmentSlotsParams for details.

        Returns:
            dict: The API response containing the available appointment slots.

        Raises:
            Exception: If retrieving appointment slots fails.
        """
        try:
            get_appointment_slots = GetAppointmentSlotsParams(**kwargs)
            response = get_available_appointment_slots(
                api_key=self.api_key, params=get_appointment_slots, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to get available appointment slots: {e}")
            raise

    @type_hint_from_params(CreateAppointmentParams)
    def create_appointment(self, retries=0, retry_delay=500, **kwargs):
        """
        Create a new appointment using the provided parameters.

        Args:
            **kwargs: Parameters required for creating an appointment. Refer to CreateAppointmentParams for details.

        Returns:
            dict: The API response containing the created appointment information.

        Raises:
            Exception: If the appointment creation fails.
        """
        try:
            create_appointment_params = CreateAppointmentParams(**kwargs)
            response = create_appointment(
                api_key=self.api_key, params=create_appointment_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to create appointment: {e}")
            raise

    @type_hint_from_params(GetAppointmentByIdParams)
    def get_appointment_by_id(self, retries=3, retry_delay=500, **kwargs):
        """
        Retrieve an appointment by its unique identifier.

        Args:
            appointment_id (str): The unique identifier of the appointment.

        Returns:
            dict: The API response containing the appointment information.

        Raises:
            Exception: If the appointment retrieval fails.
        """
        try:
            get_appointment_by_id_params = GetAppointmentByIdParams(**kwargs)
            response = get_appointment_by_id(
                api_key=self.api_key, params=get_appointment_by_id_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to get appointment by id: {e}")
            raise

    @type_hint_from_params(GetAppointmentsParams)
    def get_appointments(self, retries=3, retry_delay=500, **kwargs):
        """
        Retrieve appointments based on the provided parameters.

        Args:
            **kwargs: Parameters for retrieving appointments. Refer to GetAppointmentsParams for details.

        Returns:
            dict: The API response containing the appointments information.

        Raises:
            Exception: If retrieving appointments fails.
        """
        try:
            get_appointments_params = GetAppointmentsParams(**kwargs)
            response = get_appointments(
                api_key=self.api_key, params=get_appointments_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to get appointments: {e}")
            raise

    @type_hint_from_params(DeleteAppointmentParams)
    def delete_appointment(self, retries=0, retry_delay=500, **kwargs):
        """
        Delete an appointment using the provided parameters.

        Args:
            **kwargs: Parameters for deleting an appointment. Refer to DeleteAppointmentParams for details.

        Raises:
            Exception: If the appointment deletion fails.
        """
        try:
            delete_appointment_params = DeleteAppointmentParams(**kwargs)
            response = delete_appointment(
                api_key=self.api_key, params=delete_appointment_params, retries=retries, retry_delay=retry_delay
            )
            return response
        except Exception as e:
            logger.debug(f"Failed to delete appointment: {e}")
            raise

    @type_hint_from_params(UpdateAppointmentParams)
    def update_appointment(self, retries=0, retry_delay=500, **kwargs):
        """
        Update an existing appointment using the provided parameters.

        Args:
            **kwargs: Parameters for updating an appointment. Refer to UpdateAppointmentParams for details.

        Returns:
            dict: The API response containing the updated appointment information.

        Raises:
            Exception: If the appointment update fails.
        """
        try:
            update_appointment_params = UpdateAppointmentParams(**kwargs)
            response = update_appointment(
                api_key=self.api_key, params=update_appointment_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to update appointment: {e}")
            raise

    @type_hint_from_params(UpdateAppointmentStatusParams)
    def update_appointment_status(self, retries=0, retry_delay=500, **kwargs):
        """
        Update the status of an appointment.

        Args:
            **kwargs: Parameters for updating the appointment status. Refer to UpdateAppointmentStatusParams for details.

        Returns:
            dict: The API response confirming the status update.

        Raises:
            Exception: If the status update fails.
        """
        try:
            update_appointment_status_params = UpdateAppointmentStatusParams(**kwargs)
            response = update_appointment_status(
                api_key=self.api_key, params=update_appointment_status_params, retries=retries, retry_delay=retry_delay
            )
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to update appointment status: {e}")
            raise

    #######################################
    # Workflows Endpoints
    #######################################
    @type_hint_from_params(GetWorkflowsParams)
    def get_workflows(self, retries=3, retry_delay=500, **kwargs):
        """
        Retrieve workflows using the provided parameters.

        Args:
            **kwargs: Parameters for retrieving workflows. Refer to GetWorkflowsParams for details.

        Returns:
            dict: The API response containing the workflows information.

        Raises:
            Exception: If retrieving workflows fails.
        """
        try:
            get_workflows_params = GetWorkflowsParams(**kwargs)
            response = get_workflows(api_key=self.api_key, params=get_workflows_params, retries=retries, retry_delay=retry_delay)
            return response.json()
        except Exception as e:
            logger.debug(f"Failed to get workflows: {e}")
            raise

    #######################################
    # Async Wrappers
    #######################################

    async def get_coroutine(self, func, *args, **kwargs):
        """
        Run a synchronous function in an executor to make it non-blocking.

        Args:
            func (Callable): The function to execute asynchronously.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            Coroutine: The coroutine that executes the function asynchronously.
        """

        return await asyncio.to_thread(func, *args, **kwargs)

    async def create_contact_async(self, retries=0, retry_delay=500, **kwargs):
        """Asynchronously create a contact."""
        return await self.get_coroutine(self.create_contact, retries=retries, retry_delay=retry_delay, **kwargs)

    async def lookup_contact_async(self, retries=3, retry_delay=500, **kwargs):
        """Asynchronously lookup a contact."""
        return await self.get_coroutine(self.lookup_contact, retries=retries, retry_delay=retry_delay, **kwargs)

    async def get_contact_by_id_async(self, retries=3, retry_delay=500, **kwargs):
        """Asynchronously retrieve a contact by ID."""
        return await self.get_coroutine(self.get_contact_by_id, retries=retries, retry_delay=retry_delay, **kwargs)

    async def update_contact_async(self, retries=2, retry_delay=1000, **kwargs):
        """Asynchronously update a contact."""
        return await self.get_coroutine(self.update_contact, retries=retries, retry_delay=retry_delay, **kwargs)

    async def delete_contact_async(self, retries=0, retry_delay=500, **kwargs):
        """Asynchronously delete a contact."""
        return await self.get_coroutine(self.delete_contact, retries=retries, retry_delay=retry_delay, **kwargs)

    async def get_contact_appointments_async(self, retries=3, retry_delay=500, **kwargs):
        """Asynchronously retrieve contact appointments."""
        return await self.get_coroutine(self.get_contact_appointments, retries=retries, retry_delay=retry_delay, **kwargs)

    async def tag_contact_async(self, retries=0, retry_delay=500, **kwargs):
        """Asynchronously add tags to a contact."""
        return await self.get_coroutine(self.tag_contact, retries=retries, retry_delay=retry_delay, **kwargs)

    async def remove_tag_from_contact_async(self, retries=0, retry_delay=500, **kwargs):
        """Asynchronously remove tags from a contact."""
        return await self.get_coroutine(self.remove_tag_from_contact, retries=retries, retry_delay=retry_delay, **kwargs)

    async def add_contact_to_workflow_async(self, retries=0, retry_delay=500, **kwargs):
        """Asynchronously add a contact to a workflow."""
        return await self.get_coroutine(self.add_contact_to_workflow, retries=retries, retry_delay=retry_delay, **kwargs)

    async def get_available_appointment_slots_async(self, retries=3, retry_delay=500, **kwargs):
        """Asynchronously retrieve available appointment slots."""
        return await self.get_coroutine(self.get_available_appointment_slots, retries=retries, retry_delay=retry_delay, **kwargs)

    async def create_appointment_async(self, retries=0, retry_delay=500, **kwargs):
        """Asynchronously create an appointment."""
        return await self.get_coroutine(self.create_appointment, retries=retries, retry_delay=retry_delay, **kwargs)

    async def get_appointment_by_id_async(self, retries=3, retry_delay=500, **kwargs):
        """Asynchronously retrieve an appointment by ID."""
        return await self.get_coroutine(self.get_appointment_by_id, retries=retries, retry_delay=retry_delay, **kwargs)

    async def get_appointments_async(self, retries=3, retry_delay=500, **kwargs):
        """Asynchronously retrieve appointments."""
        return await self.get_coroutine(self.get_appointments, retries=retries, retry_delay=retry_delay, **kwargs)

    async def delete_appointment_async(self, retries=0, retry_delay=500, **kwargs):
        """Asynchronously delete an appointment."""
        return await self.get_coroutine(self.delete_appointment, retries=retries, retry_delay=retry_delay, **kwargs)

    async def update_appointment_async(self, retries=0, retry_delay=500, **kwargs):
        """Asynchronously update an appointment."""
        return await self.get_coroutine(self.update_appointment, retries=retries, retry_delay=retry_delay, **kwargs)

    async def update_appointment_status_async(self, retries=0, retry_delay=500, **kwargs):
        """Asynchronously update appointment status."""
        return await self.get_coroutine(self.update_appointment_status, retries=retries, retry_delay=retry_delay, **kwargs)

    async def get_workflows_async(self, retries=3, retry_delay=500, **kwargs):
        """Asynchronously retrieve workflows."""
        return await self.get_coroutine(self.get_workflows, retries=retries, retry_delay=retry_delay, **kwargs)

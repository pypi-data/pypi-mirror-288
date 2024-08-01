from __future__ import annotations

from datetime import datetime, timedelta

from pydantic import Field, EmailStr, HttpUrl, constr, StrictStr, validator
from typing import Optional, List, Dict
from src.leadmo_api.models.common import BaseLeadmoApiCallModel

# class AppointmentDetails(BaseLeadmoApiCallModel):
#     pass


class GetAppointmentSlots(BaseLeadmoApiCallModel):
    calendar_id: StrictStr
    start_date: StrictStr = Field(
        default_factory=lambda: str(int(datetime.utcnow().timestamp() * 1000)), description="Epoch timestamp"
    )
    end_date: StrictStr = Field(
        default_factory=lambda: str(int((datetime.utcnow() + timedelta(weeks=1)).timestamp() * 1000)),
        description="Epoch timestamp",
    )

    user_id: Optional[StrictStr] = Field(None, description="User ID")
    timezone: Optional[StrictStr] = Field("US/Eastern", description="Timezone for the start and end dates")


class CreateAppointment(BaseLeadmoApiCallModel):
    # One of these must be provided
    email: Optional[EmailStr] = Field(None, description="Email of the contact")
    phone: Optional[constr(pattern=r"^\+?[1-9]\d{1,14}$")] = Field(None, description="Phone number of the contact")

    # Required
    selected_slot: StrictStr = Field(
        ..., description="The selected slot for the appointment - example: 2021-02-05T11:00:00+05:30"
    )
    selected_timezone: StrictStr = Field(
        "US/Eastern", description="The selected timezone for the appointment - default: US/Eastern"
    )
    calendar_id: StrictStr = Field(..., description="The calendar ID for the appointment")

    # Optional
    title: Optional[str] = None
    first_name: Optional[StrictStr] = None
    last_name: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
    address1: Optional[StrictStr] = None
    city: Optional[StrictStr] = None
    state: Optional[StrictStr] = None
    website: Optional[HttpUrl] = None
    custom_field: Optional[Dict[StrictStr, StrictStr]] = None
    calendar_notes: Optional[StrictStr] = None

    @validator("custom_field", pre=True, each_item=True)
    def check_not_empty(cls, v):
        if v is not None and isinstance(v, str) and not v.strip():
            raise ValueError("Empty strings are not allowed")
        return v

    def __post_init__(self):
        if self.email is None and self.phone is None:
            raise ValueError("One of contact_id, email or phone must be provided")


class GetAppointmentById(BaseLeadmoApiCallModel):
    # One of these must be provided
    appointment_id: Optional[StrictStr] = Field(None, description="The appointment ID")


class GetAppointments(BaseLeadmoApiCallModel):
    start_date: StrictStr = Field(
        default_factory=lambda: str(int(datetime.utcnow().timestamp() * 1000)), description="Epoch timestamp"
    )
    end_date: StrictStr = Field(
        default_factory=lambda: str(int((datetime.utcnow() + timedelta(weeks=1)).timestamp() * 1000)),
        description="Epoch timestamp",
    )

    calendar_id: Optional[StrictStr] = Field(None, description="The calendar ID for the appointments to get")
    team_id: Optional[StrictStr] = Field(None, description="The team ID for the appointments to get")
    user_id: Optional[StrictStr] = Field(None, description="The user ID associated with the appointments to retrieve")

    include_all: Optional[bool] = Field(False, description="Include contact and more data")

    def __post_init__(self):
        if self.calendar_id is None and self.team_id is None and self.user_id is None:
            raise ValueError("One of user_id, team_id, or calendar_id must be provided")


class DeleteAppointment(BaseLeadmoApiCallModel):
    # One of these must be provided
    appointment_id: StrictStr = Field(None, description="The appointment ID")


class UpdateAppointment(BaseLeadmoApiCallModel):
    appointment_id: StrictStr = Field(..., description="The appointment ID")

    # Optional
    selected_slot: Optional[StrictStr] = Field(
        None, description="The selected slot for the appointment - example: 2021-02-05T11:00:00+05:30"
    )
    selected_timezone: Optional[StrictStr] = Field(
        "US/Eastern", description="The selected timezone for the appointment - default: US/Eastern"
    )
    calendar_notes: Optional[StrictStr] = Field(None, description="Notes for the appointment")


class UpdateAppointmentStatus(BaseLeadmoApiCallModel):
    appointment_id: StrictStr = Field(..., description="The appointment ID")
    status: StrictStr = Field("confirmed", description="The status of the appointment")

    def __post_init__(self):
        valid_statuses = ["confirmed", "cancelled", "showed", "noshow", "invalid"]
        if self.status not in valid_statuses:
            raise ValueError("status must be one of 'confirmed', 'cancelled', or 'rescheduled'")


#

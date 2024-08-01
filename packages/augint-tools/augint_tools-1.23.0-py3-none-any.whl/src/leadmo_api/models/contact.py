from __future__ import annotations
from pydantic import Field, EmailStr, HttpUrl, constr, StrictStr, validator
from typing import Optional, List, Dict
from src.leadmo_api.models.common import BaseLeadmoApiCallModel


class ContactDetails(BaseLeadmoApiCallModel):
    location_id: Optional[StrictStr] = Field(None, description="Location ID")
    email: Optional[EmailStr] = Field(None, description="Email of the contact")
    phone: Optional[constr(pattern=r"^\+?[1-9]\d{1,14}$")] = Field(None, description="Phone number of the contact")
    first_name: Optional[StrictStr] = Field(None, description="The contact's first name")
    last_name: Optional[StrictStr] = Field(None, description="The contact's last name")
    name: Optional[StrictStr] = Field(None, description="The contact's full name")
    address1: Optional[StrictStr] = Field(None, description="The contact's address line 1")
    city: Optional[StrictStr] = Field(None, description="The contact's city")
    state: Optional[StrictStr] = Field(None, description="The contact's state")
    postal_code: Optional[StrictStr] = Field(None, description="The contact's postal code")
    website: Optional[HttpUrl] = Field(None, description="The contact's website")
    timezone: Optional[StrictStr] = Field(None, description="The contact's timezone")
    dnd: Optional[bool] = Field(None, description="The contact's do not disturb status")
    tags: Optional[List[StrictStr]] = Field(None, description="The contact's tags")
    custom_field: Optional[Dict[StrictStr, StrictStr]] = Field(None, description="The contact's custom fields")
    source: Optional[StrictStr] = Field(None, description="The contact's source")

    @validator("tags", "custom_field", pre=True, each_item=True)
    def check_not_empty(cls, v):
        if v is not None and isinstance(v, str) and not v.strip():
            raise ValueError("Empty strings are not allowed")
        return v


class CreateContact(ContactDetails):
    email: Optional[EmailStr] = Field(None, description="Email of the contact")
    phone: Optional[constr(pattern=r"^\+?[1-9]\d{1,14}$")] = Field(None, description="Phone number of the contact")


class UpdateContact(ContactDetails):
    email: Optional[EmailStr] = Field(None, description="Email of the contact")
    phone: Optional[constr(pattern=r"^\+?[1-9]\d{1,14}$")] = Field(None, description="Phone number of the contact")
    contact_id: Optional[StrictStr] = Field(None, description="The contact's id")

    def __post_init__(self):
        if self.contact_id is None and self.email is None and self.phone is None:
            raise ValueError("One of contact_id, email or phone must be provided")


class LookupContact(BaseLeadmoApiCallModel):
    email: Optional[EmailStr] = Field(None, description="Email of the contact")
    phone: Optional[constr(pattern=r"^\+?[1-9]\d{1,14}$")] = Field(None, description="Phone number of the contact")


class GetContactById(BaseLeadmoApiCallModel):
    contact_id: Optional[StrictStr] = Field(None, description="The contact's id")


class DeleteContact(BaseLeadmoApiCallModel):
    email: Optional[EmailStr] = Field(None, description="Email of the contact")
    phone: Optional[constr(pattern=r"^\+?[1-9]\d{1,14}$")] = Field(None, description="Phone number of the contact")
    contact_id: Optional[constr(min_length=12, max_length=32)] = Field(None, description="The contact's id")

    def __post_init__(self):
        if self.contact_id is None and self.email is None and self.phone is None:
            raise ValueError("One of contact_id, email or phone must be provided")

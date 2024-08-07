from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .base_response import ApiResponse


class Contact(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    workspace_id: int

    company_name: Optional[str] = None
    company_registration_number: Optional[str] = None
    country_code: Optional[str] = None
    created_time: Optional[datetime] = None
    date_of_birth: Optional[str] = None
    notes: Optional[str] = None
    phone_number: Optional[str] = None
    title: Optional[str] = None
    updated_time: Optional[datetime] = None


class ContactsResponse(ApiResponse[Contact]):
    pass

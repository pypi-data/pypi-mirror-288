from pydantic import BaseModel, HttpUrl
from typing import Any, Optional, List, Dict, TypeVar, Generic
from datetime import datetime
from .base_response import Link, ApiResponse


class Permissions(BaseModel):
    contract_create: bool = False


class Workspace(BaseModel):
    _integration_permissions: List[Dict[str, Any]] = []
    _links: Dict[str, Link]
    _permissions: Permissions
    company_name: str
    country_code: str
    created_time: datetime
    date_format: str
    description: str
    id: int
    name: str
    registration_number: str
    type: str
    updated_time: datetime


class WorkspacesResponse(ApiResponse[Workspace]):
    pass

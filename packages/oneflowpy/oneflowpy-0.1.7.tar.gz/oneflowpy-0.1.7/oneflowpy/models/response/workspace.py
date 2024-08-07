from pydantic import BaseModel
from typing import Any, List, Dict, Optional
from datetime import datetime
from .base_response import Link, ApiResponse, Permissions


class Workspace(BaseModel):
    _integration_permissions: List[Dict[str, Any]] = []
    _links: Dict[str, Link] = {}
    id: int
    name: str
    _permissions: Optional[Permissions] = None
    company_name: Optional[str] = None
    country_code: Optional[str] = None
    created_time: Optional[datetime] = None
    date_format: Optional[str] = None
    description: Optional[str] = None
    registration_number: Optional[str] = None
    type: Optional[str] = None
    updated_time: Optional[datetime] = None


class WorkspacesResponse(ApiResponse[Workspace]):
    pass

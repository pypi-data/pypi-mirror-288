from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime
from .base_response import Link, Permissions, ApiResponse
from .workspace import Workspace


class DeliveryChannel(BaseModel):
    name: str
    preferred: bool
    required_participant_attributes: List[str]


class SignMethod(BaseModel):
    name: str
    preferred: bool


class TwoStepAuthenticationMethod(BaseModel):
    name: str
    preferred: bool
    required_participant_attributes: List[str]


class AvailableOptions(BaseModel):
    can_receive_attachments: bool
    can_receive_expanded_pdf: bool
    can_receive_products: bool
    delivery_channels: List[DeliveryChannel]
    sign_methods: List[SignMethod]
    two_step_authentication_methods: List[TwoStepAuthenticationMethod]


class DefaultCreatorRoles(BaseModel):
    _permissions: Permissions
    organizer: bool
    signatory: bool


class Configuration(BaseModel):
    default_creator_roles: DefaultCreatorRoles


class TemplateType(BaseModel):
    created_time: datetime
    description: str
    extension_type: str
    id: int
    name: str
    updated_time: datetime


class Tag(BaseModel):
    id: int
    name: str


class Template(BaseModel):
    _links: Optional[Dict[str, Link]]
    available_options: AvailableOptions
    configuration: Configuration
    created_time: datetime
    id: int
    name: str
    tags: List[Tag]
    template_active: bool
    template_type: Optional[TemplateType]
    updated_time: datetime
    workspaces: List[Workspace]


class TemplatesResponse(ApiResponse[Template]):
    pass

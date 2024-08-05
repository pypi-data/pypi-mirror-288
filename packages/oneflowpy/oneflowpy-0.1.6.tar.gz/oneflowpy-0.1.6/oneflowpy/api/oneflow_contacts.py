from typing import Any, Dict, List
from .oneflow_crud import OneflowCRUD
from ..models import Contact, ContactsResponse


class OneflowContacts(OneflowCRUD):

    _resource_path = "contacts"
    _datamodel = Contact
    _list_response = ContactsResponse

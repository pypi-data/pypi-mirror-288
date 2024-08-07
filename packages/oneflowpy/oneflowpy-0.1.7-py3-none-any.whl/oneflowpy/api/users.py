from .crud import OneflowCRUD
from oneflowpy.models import UsersResponse, User


class OneflowUsers(OneflowCRUD):
    _resource_path = "users"
    _datamodel = User
    _list_response = UsersResponse
    _uses_workspace = False

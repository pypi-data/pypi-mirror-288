from typing import Any, Dict, List
from .crud import OneflowCRUD
from ..models import WorkspacesResponse, Workspace


class OneflowWorkspaces(OneflowCRUD):

    _resource_path = "workspaces"
    _datamodel = Workspace
    _list_response = WorkspacesResponse
    _uses_workspace = False

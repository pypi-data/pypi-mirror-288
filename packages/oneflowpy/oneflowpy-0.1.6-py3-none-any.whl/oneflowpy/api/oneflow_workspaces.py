from typing import Any, Dict, List

from pydantic import BaseModel
from .oneflow_crud import OneflowCRUD
from ..models import WorkspacesResponse, Workspace


class OneflowWorkspaces(OneflowCRUD):

    _resource_path = "workspaces"
    _datamodel = Workspace
    _list_response = WorkspacesResponse

    def list(self, **kwargs) -> List[Dict[str, Any]]:
        kwargs["params"] = None
        return super().list(**kwargs)

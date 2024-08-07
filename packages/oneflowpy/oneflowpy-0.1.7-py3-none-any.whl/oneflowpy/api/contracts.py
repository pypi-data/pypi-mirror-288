from typing import Any, Dict, List
from .crud import OneflowCRUD
from oneflowpy.models import Contract, ContractsResponse


class OneflowContracts(OneflowCRUD):

    _resource_path = "contracts"
    _datamodel = Contract
    _list_response = ContractsResponse

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel
from .oneflow_client import OneflowClient
from ..models import ApiResponse

# i need to create iterator for the list method or the response object


class OneflowCRUD(ABC):
    """
    Abstract base class for implementing LCRUD operations against the Oneflow API.
    """

    _resource_path: Optional[str] = None
    _datamodel: Optional[BaseModel] = None
    _list_response: Optional[ApiResponse] = None

    def __init__(self, client: OneflowClient, workspace_id: str) -> None:
        self.client = client
        self.workspace_id = workspace_id

    def model_validator(self, data: Union[Dict[str, Any], BaseModel]) -> BaseModel:
        """
        Validates the data against the Pydantic data model. This method handles both dictionary inputs
        and model instances. If a dictionary is provided, it validates and converts it to the model.
        If a model instance is provided, it re-validates it (useful if the model was modified).

        Parameters:
            data (Union[Dict[str, Any], BaseModel]): The data to validate, either as a dictionary or a model instance.

        Returns:
            BaseModel: The validated and possibly transformed Pydantic model instance.
        """
        if isinstance(data, Dict):
            # Convert dictionary to Pydantic model instance
            return self.datamodel(**data)
        elif isinstance(data, self.datamodel):
            # Re-validate model instance, useful if already instantiated but needs re-validation
            return self.datamodel(**data.dict())
        else:
            raise TypeError(
                "Input must be a dictionary or an instance of the defined data model"
            )

    @property
    def resource_path(self) -> str:
        """
        Defines the specific path of the resource relative to the company slug.
        Must be implemented by subclasses to return the resource-specific part of the URL.
        """
        assert (
            self._resource_path is not None
        ), "Resource path must be defined in subclass"
        return self._resource_path

    @property
    def datamodel(self) -> BaseModel:
        """
        Returns the Pydantic data model for the resource.
        Must be implemented by subclasses to return the appropriate Pydantic model.
        """
        assert self._datamodel is not None, "Data model must be defined in subclass"
        return self._datamodel

    @property
    def list_response(self) -> ApiResponse:
        """
        Returns the response object for the list method.
        Must be implemented by subclasses to return the appropriate response object.
        """
        assert (
            self._list_response is not None
        ), "List response object must be defined in subclass"
        return self._list_response

    def list(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Retrieves a list of objects from the resource's collection.

        Returns:
            List[Dict[str, Any]]: A list of objects from the resource.
        """
        endpoint = f"{self.resource_path}"
        kwargs["params"] = kwargs.get("params", {"workspace_id": self.workspace_id})
        response = self.client.get(endpoint=endpoint, **kwargs)
        return self._list_response.model_validate(response)

    def read(self, object_id: str) -> Dict[str, Any]:
        """
        Retrieves a single object by its ID.

        Parameters:
            object_id (str): The ID of the object to retrieve.

        Returns:
            Dict[str, Any]: The object data.
        """
        endpoint = f"{self.resource_path}/{object_id}"
        response = self.client.get(endpoint=endpoint)
        return self.datamodel.model_validate(response)

    def delete(self, object_id: str) -> None:
        """
        Deletes an object identified by its ID.

        Parameters:
            object_id (str): The ID of the object to delete.
        """
        endpoint = f"{self.resource_path}/{object_id}"
        self.client.delete(endpoint)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a new object with the provided data.
        Must be implemented by subclasses due to potentially varying data structures.

        Parameters:
            data (Dict[str, Any]): Data for creating the new object.

        Returns:
            Dict[str, Any]: The created object data.
        """
        data["workspace_id"] = data.get("workspace_id", self.workspace_id)
        validated_data = self.model_validator(data)
        endpoint = f"{self.resource_path}"
        return self.client.post(
            endpoint, data=validated_data.model_dump(exclude_none=True)
        )

    def update(self, object_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates an existing object identified by its ID with the given data.
        Must be implemented by subclasses due to potentially varying data structures.

        Parameters:
            object_id (str): The ID of the object to update.
            data (Dict[str, Any]): New data for updating the object.

        Returns:
            Dict[str, Any]: The updated object data.
        """
        pass

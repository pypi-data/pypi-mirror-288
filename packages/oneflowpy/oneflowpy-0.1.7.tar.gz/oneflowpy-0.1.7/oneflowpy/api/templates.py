from typing import Any, Dict, List
from .crud import OneflowCRUD
from oneflowpy.models import Template, TemplatesResponse


class OneflowTemplates(OneflowCRUD):
    _resource_path = "templates"
    _datamodel = Template
    _list_response = TemplatesResponse
    _uses_workspace = False

    def read_file(
        self, object_id: str, file_id: str, download: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieves a single object file by its ID.

        Parameters:
            object_id (str): The ID of the object to retrieve.
            file_id (str): The ID of the file to retrieve.

        Returns:
            Dict[str, Any]: The object data.
        """
        endpoint = f"{self.resource_path}/{object_id}/files/{file_id}"
        response = self.client.get(endpoint=endpoint, params={"download": download})

        return response

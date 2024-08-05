import os
from typing import Any, Optional
from .oneflow_client import OneflowClient
from .oneflow_contacts import OneflowContacts
from .oneflow_workspaces import OneflowWorkspaces


# i need to create context manager for the api class


class OneflowAPI:
    """
    Main class to interact with the Oneflow API, providing access to various
    resources like contacts, contracts and more through a unified interface.
    It attempts to retrieve the access token from an environment variable;
    if not available, the token must be passed explicitly.
    """

    def __init__(
        self,
        workspace_id: str,
        api_key: Optional[str] = None,
        user_email: Optional[str] = None,
    ) -> None:
        """
        Initializes the OneflowAPI with the necessary authentication token and company slug.
        Attempts to use the access token from the environment variable API_KEY
        if not explicitly passed.

        Parameters:
            workspace_id (str): The workspace to perform operations for.
            api_key (Optional[str]): The API_KEY to authenticate against the Oneflow API.
            user_email (Optional[str]): The email of the user to authenticate as.
                                          If api_key or user_email not provided, attempts to fetch from environment.
        """

        self.client = OneflowClient()
        self.client.validate_auth_headers(api_key, user_email)
        self.client.set_auth_headers()
        self.workspace_id = workspace_id

        # Initialize resource-specific handlers
        self.workspaces = OneflowWorkspaces(self.client, self.workspace_id)
        self.contacts = OneflowContacts(self.client, self.workspace_id)

        # Add other resource handlers as needed, e.g., self.contacts, self.products, etc.

    def use_custom_resource(self, resource_class: Any, *args, **kwargs) -> Any:
        """
        Allows for the dynamic use of custom resources that follow the OneflowCRUD structure,
        enabling the extension of the API without modifying the core OneflowAPI class.

        Parameters:
            resource_class (Any): The class of the custom resource to be instantiated.
            *args: Positional arguments to pass to the resource class constructor.
            **kwargs: Keyword arguments to pass to the resource class constructor.

        Returns:
            An instance of the specified resource class, initialized with the provided arguments.
        """
        return resource_class(self.client, self.workspace_id, *args, **kwargs)

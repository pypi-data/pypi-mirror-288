""" This module contains the BaseClient class for handling common HTTP operations and token management. """
import os
import requests
from dotenv import load_dotenv
from modelhub.utils import setup_logger, handle_response, ModelHubException

load_dotenv()

logger = setup_logger(__name__)


class BaseClient:
    """Base client for handling common HTTP operations and token management."""

    def __init__(self, base_url, client_id=None, client_secret=None, token=None):
        """
        Initializes a new instance of the BaseClient class.

        Args:
            base_url (str): The base URL of the API.
            client_id (str, optional): The client ID for authentication. Defaults to None.
            client_secret (str, optional): The client secret for authentication. Defaults to None.
            token (str, optional): The access token for authentication. Defaults to None.
        """
        self.base_url = base_url
        self.modelhub_url = f"{base_url}/modelhub/api/v1"
        self.auth_url = f"{base_url}/ums/api/v1"
        self.client_id = client_id or os.getenv("MODELHUB_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("MODELHUB_CLIENT_SECRET")
        self.token = token or os.getenv("MODELHUB_TOKEN")
        self.headers = {}

        if self.token and self.token.strip():
            self.headers = {"Authorization": f"{self.token}"}
        elif (
            self.client_id
            and self.client_secret
            and self.client_id.strip()
            and self.client_secret.strip()
        ):
            self.get_token()

    def get_token(self):
        """
        Fetches a token using the client credentials flow and stores it in self.token.
        """
        token_endpoint = f"{self.auth_url}/auth/get-token"
        headers = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "content-type": "application/json",
        }
        response = requests.post(token_endpoint, headers=headers, timeout=10)
        response_data = handle_response(response)
        if "token" in response_data:
            self.token = response_data.get("token").get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            raise ModelHubException("Token not found in response data")

    def request_with_retry(self, method, endpoint, **kwargs):
        """
        Sends a request and retries with a new token if a 401 Unauthorized response is received.

        Args:
            method (str): The HTTP method for the request.
            endpoint (str): The endpoint to send the request to.
            **kwargs: Additional keyword arguments to be passed to the requests library.

        Returns:
            dict: The response data.

        Raises:
            ModelHubException: If the token is not found in the response data.
        """
        url = f"{self.modelhub_url}/{endpoint}"
        logger.debug("headers: %s", self.headers)
        response = requests.request(
            method, url, headers=self.headers, **kwargs, timeout=10
        )

        if response.status_code == 401 and self.client_id and self.client_secret:
            self.get_token()
            kwargs["headers"] = self.headers
            response = requests.request(method, url, **kwargs, timeout=10)

        return handle_response(response)

    def post(self, endpoint, json=None, params=None, files=None, data=None):
        """
        Sends a POST request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.
            json (dict, optional): The JSON payload for the request. Defaults to None.
            params (dict, optional): The query parameters for the request. Defaults to None.
            files (dict, optional): The files to be uploaded with the request. Defaults to None.
            data (dict, optional): The form data for the request. Defaults to None.

        Returns:
            dict: The response data.
        """
        return self.request_with_retry(
            "post", endpoint, json=json, params=params, files=files, data=data
        )

    def get(self, endpoint, params=None):
        """
        Sends a GET request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.
            params (dict, optional): The query parameters for the request. Defaults to None.

        Returns:
            dict: The response data.
        """
        return self.request_with_retry("get", endpoint, params=params)

    def put(self, endpoint, json=None):
        """
        Sends a PUT request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.
            json (dict, optional): The JSON payload for the request. Defaults to None.

        Returns:
            dict: The response data.
        """
        return self.request_with_retry("put", endpoint, json=json)

    def delete(self, endpoint):
        """
        Sends a DELETE request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the request to.

        Returns:
            dict: The response data.
        """
        return self.request_with_retry("delete", endpoint)

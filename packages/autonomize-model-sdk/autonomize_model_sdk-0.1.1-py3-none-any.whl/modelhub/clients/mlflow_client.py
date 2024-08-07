""" Client for interacting with MLflow. """

import os
from contextlib import contextmanager
import mlflow
from modelhub.core import BaseClient


class MLflowClient(BaseClient):
    """Client for interacting with MLflow."""

    def __init__(self, base_url, client_id=None, client_secret=None, token=None):
        """
        Initialize the MLflowClient.

        Args:
            base_url (str): The base URL of the MLflow server.
            client_id (str, optional): The client ID for authentication. Defaults to None.
            client_secret (str, optional): The client secret for authentication. Defaults to None.
            token (str, optional): The access token for authentication. Defaults to None.
        """
        super().__init__(base_url, client_id, client_secret, token)
        self.configure_mlflow()

    def configure_mlflow(self):
        """
        Configure MLflow settings.

        This method retrieves the MLflow tracking URI and credentials from the server
        and sets them in the MLflow library and environment variables.
        """
        response = self.get("mlflow/tracking_uri")
        tracking_uri = response.get("tracking_uri")
        mlflow.set_tracking_uri(tracking_uri)

        response = self.get("mlflow/credentials")
        username = response.get("username")
        password = response.get("password")

        if username and password:
            mlflow.set_tracking_uri(tracking_uri)
            mlflow.set_registry_uri(tracking_uri)
            os.environ["MLFLOW_TRACKING_USERNAME"] = username
            os.environ["MLFLOW_TRACKING_PASSWORD"] = password

    @contextmanager
    def start_run(self, run_name=None, nested=False, tags=None, output_path="/tmp"):
        """
        Context manager for starting an MLflow run.

        Args:
            run_name (str, optional): The name of the run. Defaults to None.
            nested (bool, optional): Whether the run is nested. Defaults to False.
            tags (dict, optional): Additional tags for the run. Defaults to None.
            output_path (str, optional): The output path for storing the run ID. Defaults to "/tmp".

        Yields:
            mlflow.ActiveRun: The active MLflow run.

        Raises:
            OSError: If the output path cannot be created.
        """
        os.makedirs(output_path, exist_ok=True)  # Ensure the output path exists
        with mlflow.start_run(run_name=run_name, nested=nested, tags=tags) as run:
            run_id = run.info.run_id
            run_id_path = os.path.join(output_path, "run_id")
            with open(run_id_path, "w", encoding="utf-8") as f:
                f.write(run_id)
            yield run

    def get_previous_stage_run_id(self, output_path="/tmp"):
        """
        Get the run ID of the previous stage.

        Args:
            output_path (str, optional): The output path where the run ID is stored. Defaults to "/tmp".

        Returns:
            str: The run ID of the previous stage.

        Raises:
            FileNotFoundError: If the run ID file is not found.
        """
        run_id_path = os.path.join(output_path, "run_id")
        with open(run_id_path, "r", encoding="utf-8") as f:
            run_id = f.read().strip()
        return run_id

""" Client for interacting with MLflow. """

import os
from contextlib import contextmanager
from typing import Optional
import mlflow
from ..core import BaseClient


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

    def end_run(self, status="FINISHED"):
        """
        End the current MLflow run.
        """
        mlflow.end_run(status=status)

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

    def set_experiment(self, experiment_name: Optional[str] = None, experiment_id: Optional[str] = None):
        """
        Set the active experiment.

        Args:
            experiment_name (str): The name of the experiment.
            experiment_id (str): The ID of the experiment.
        """
        mlflow.set_experiment(experiment_name, experiment_id)

    def log_param(self, key, value):
        """
        Log a parameter.

        Args:
            key (str): The parameter key.
            value (str): The parameter value.
        """
        mlflow.log_param(key, value)

    def log_metric(self, key, value):
        """
        Log a metric.

        Args:
            key (str): The metric key.
            value (float): The metric value.
        """
        mlflow.log_metric(key, value)

    def log_artifact(self, local_path: str, artifact_path: Optional[str] = None, run_id: Optional[str] = None):
        """
        Log an artifact.

        Args:
            local_path (str): The local path of the artifact.
            artifact_path (str, optional): The artifact path. Defaults to None.
            run_id (str, optional): The run ID. Defaults to None.
        """
        mlflow.log_artifact(local_path, artifact_path, run_id)

    def get_run(self, run_id):
        """
        Get the run details.

        Args:
            run_id (str): The ID of the run.

        Returns:
            dict: The run details.
        """
        return mlflow.get_run(run_id).to_dictionary()

    def get_artifact_uri(self, run_id):
        """
        Get the artifact URI for the run.

        Args:
            run_id (str): The ID of the run.

        Returns:
            str: The artifact URI.
        """
        return mlflow.get_artifact_uri(run_id)

    def load_model(self, model_uri):
        """
        Load the model from the specified URI.

        Args:
            model_uri (str): The URI of the model.

        Returns:
            Any: The loaded model.
        """
        return mlflow.pyfunc.load_model(model_uri)

    def save_model(self, model, model_path):
        """
        Save the model to the specified path.

        Args:
            model (Any): The model to save.
            model_path (str): The path to save the model.
        """
        mlflow.pyfunc.save_model(model, model_path)
    
    @property
    def mlflow(self):
            """
            Returns the mlflow module.

            Returns:
                The mlflow module.
            """
            return mlflow

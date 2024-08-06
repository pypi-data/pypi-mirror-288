""" This module defines the ModelHubClient class, which provides a client for interacting with the ModelHub API. """

from modelhub.utils import setup_logger
from modelhub.clients import MLflowClient, PipelineManager
from modelhub.core import ModelHubException

logger = setup_logger(__name__)


class ModelHubClient:
    """A client for interacting with the ModelHub API."""

    def __init__(self, base_url, client_id=None, client_secret=None, token=None):
        """
        Initializes a ModelHubClient object.

        Args:
            base_url (str): The base URL of the ModelHub API.
            client_id (str, optional): The client ID for authentication. Defaults to None.
            client_secret (str, optional): The client secret for authentication. Defaults to None.
            token (str, optional): The authentication token. Defaults to None.
        """
        self.mlflow_client = MLflowClient(base_url, client_id, client_secret, token)
        self.pipeline_manager = PipelineManager(
            base_url, client_id, client_secret, token
        )

    def get_client(self, client_type):
        """
        Returns the client object for the specified client type.

        Args:
            client_type (str): The type of client to return.

        Returns:
            object: The client object.
        """
        if client_type == "mlflow":
            return self.mlflow_client
        elif client_type == "pipeline":
            return self.pipeline_manager
        else:
            raise ValueError(f"Invalid client type: {client_type}")

    def start_pipeline(self, config_path):
        """
        Creates or updates a pipeline using the provided configuration file.

        Args:
            config_path (str): The path to the pipeline configuration file.
        """
        pipeline = self.pipeline_manager.create_or_update(config_path)
        pipeline_id = pipeline.get("pipeline_id")
        if pipeline_id:
            logger.info("Pipeline created with ID: %s", pipeline_id)
            self.pipeline_manager.submit(pipeline_id=pipeline_id)
        else:
            logger.error("Failed to create pipeline")
            raise ModelHubException("Failed to create pipeline")
        return pipeline_id


    def start_run(self, run_name=None, nested=False, tags=None, output_path="/tmp"):
        """
        Starts a new MLflow run.

        Args:
            run_name (str, optional): The name of the run. Defaults to None.
            nested (bool, optional): Whether the run should be nested within the current run. Defaults to False.
            tags (dict, optional): Additional tags to attach to the run. Defaults to None.
            output_path (str, optional): The path where the run artifacts will be stored. Defaults to "/tmp".

        Returns:
            int: The ID of the started run.
        """
        return self.mlflow_client.start_run(run_name, nested, tags, output_path)

    def get_previous_stage_run_id(self, output_path="/tmp"):
        """
        Retrieves the ID of the previous stage run.

        Args:
            output_path (str, optional): The path where the run artifacts are stored. Defaults to "/tmp".

        Returns:
            int: The ID of the previous stage run.
        """
        return self.mlflow_client.get_previous_stage_run_id(output_path)

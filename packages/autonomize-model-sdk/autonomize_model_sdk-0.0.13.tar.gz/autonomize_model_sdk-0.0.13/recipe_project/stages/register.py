import os
from dotenv import load_dotenv
from modelhub.client import ModelHub

load_dotenv()

# Initialize the ModelHub client
modelhub_client = ModelHub(base_url=os.getenv("MODELHUB_BASE_URL"))
experiment_id = os.getenv("MLFLOW_EXPERIMENT_ID")

# Get the MLflow client from ModelHub client
mlflow = modelhub_client.create_client("mlflow")

mlflow.set_experiment(experiment_id=experiment_id)

def register_model():
    # Load model from MLflow
    model_uri = f"runs:/{os.getenv('TRAIN_RUN_ID')}/model"

    # Start an MLflow run
    with mlflow.start_run(run_name="register") as run:
        try:
            # Register the model
            model_details = mlflow.register_model(model_uri, "BERT_Model")

            # Transition the model stage to 'Production'
            client = mlflow.tracking.MlflowClient()
            client.transition_model_version_stage(
                name=model_details.name,
                version=model_details.version,
                stage="Production"
            )

            print("Model registration and transition to Production complete")

        except Exception as e:
            print(f"An error occurred: {e}")
            mlflow.end_run(status=mlflow.entities.RunStatus.FAILED)
            raise

if __name__ == "__main__":
    register_model()
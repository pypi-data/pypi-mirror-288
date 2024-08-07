import os
import logging
from sklearn.metrics import mean_squared_error, r2_score
from transformers import BertForSequenceClassification, BertTokenizer
from datasets import load_dataset
from modelhub.clients import MLflowClient
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize the MLflow client
client = MLflowClient(base_url=os.getenv("MODELHUB_BASE_URL"))
experiment_id = os.getenv("MLFLOW_EXPERIMENT_ID")

client.set_experiment(experiment_id=experiment_id)

def evaluate_model():
    # Read the run_id from the file
    run_id = client.get_previous_stage_run_id()

    logger.info("Previous stage run_id: %s", run_id)
    
    # Load dataset
    dataset = load_dataset("imdb")
    test_dataset = dataset["test"].shuffle(seed=42).select(range(100))  # Select 100 samples for quick evaluation

    # Load tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

    # Tokenize the dataset
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    test_dataset = test_dataset.map(tokenize_function, batched=True)
    test_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

    # Prepare test data
    X_test = test_dataset["input_ids"]
    y_test = test_dataset["label"]

    # Load the model using the run_id
    model_uri = f"runs:/{run_id}/model"
    model = client.load_model(model_uri)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Log metrics
    with client.start_run(run_name="evaluate") as run:
        client.log_metric("mse", mse)
        client.log_metric("r2", r2)

    print("Model evaluation complete")

if __name__ == "__main__":
    evaluate_model()
import os
import argparse
from dotenv import load_dotenv
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
from modelhub.clients import MLflowClient

load_dotenv()

# Initialize the MLflow client
client = MLflowClient(base_url=os.getenv("MODELHUB_BASE_URL"))
experiment_id = os.getenv("MLFLOW_EXPERIMENT_ID")

client.set_experiment(experiment_id=experiment_id)

def train_and_log_model(output_path: str):
    # Load dataset
    dataset = load_dataset("imdb")
    train_dataset = dataset["train"].shuffle(seed=42).select(range(100))  # Select 100 samples for quick training
    test_dataset = dataset["test"].shuffle(seed=42).select(range(100))    # Select 100 samples for quick testing

    # Load tokenizer and model
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased")

    # Tokenize the dataset
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    train_dataset = train_dataset.map(tokenize_function, batched=True)
    test_dataset = test_dataset.map(tokenize_function, batched=True)
    
    train_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    test_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./"+output_path,
        evaluation_strategy="epoch",
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=1,
        weight_decay=0.01,
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
    )

    # Start an MLflow run
    with client.start_run(run_name="train") as run:
        try:
            # Train the model
            trainer.train()

            # Log the model
            client.mlflow.transformers.log_model(trainer.model, "model")

            print("Model training and logging complete")

        except Exception as e:
            print(f"An error occurred: {e}")
            client.end_run(status="FAILED")
            raise e


if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Training")
    parser.add_argument("--output_path", type=str, required=True, help="Path to save the output data")
    
    args = parser.parse_args()
    train_and_log_model(args.output_path)
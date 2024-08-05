from openai import OpenAI
import sys
import os
import time
import logging
from typing import Dict, Any, Union, Literal
from openai.types.fine_tuning.job_create_params import Hyperparameters

COST = {
    "gpt-4o-mini-2024-07-18": 3,
    "gpt-3.5-turbo": 8
}
def train(
    dataset_path: str,
    model_name: str = "gpt-4o-mini-2024-07-18",
    batch_size: Union[Literal["auto"], int] = "auto",
    n_epochs: Union[Literal["auto"], int] = "auto",
    learning_rate_multiplier: Union[Literal["auto"], float] = "auto",
    ) -> Dict[str, Any]:
    # Set the logging level to WARNING to ignore INFO logs
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.WARNING)
    assert(os.path.isfile(dataset_path))
    assert("jsonl" in dataset_path)
    client = OpenAI()
    # Upload the dataset
    response = client.files.create(
        file=open(dataset_path, "rb"),
        purpose="fine-tune"
    )
    dataset_id = response.id
    print(f"Dataset uploaded with ID: {dataset_id}")

    # Fine-tune the model
    fine_tune_response = client.fine_tuning.jobs.create(
        training_file=dataset_id,
        model=model_name,
        hyperparameters=Hyperparameters(
            batch_size=batch_size,
            n_epochs=n_epochs,
            learning_rate_multiplier=learning_rate_multiplier
        )
    )

    print("Fine-tuning started:")
    fine_tune_job_id = fine_tune_response.id
    time_elapsed = 0
    previous_status_message_length = 0
    while True:
        status_response = client.fine_tuning.jobs.retrieve(fine_tune_job_id)
        status = status_response.status
        status_message = f"\rFine-tuning status: {status}.".ljust(previous_status_message_length)
        previous_status_message_length = len(status_message)
        sys.stdout.write(status_message)
        sys.stdout.flush()
        if status == 'succeeded':
            fine_tuned_model_name = status_response.fine_tuned_model
            print(f"\nFine-tuning succeeded. Model name: {fine_tuned_model_name}")
            print(f"Fine-tuning took {time_elapsed} seconds.")
            print(f"Fine-tuning tokens used: {status_response.trained_tokens}")
            # (base training cost per 1M input tokens ÷ 1M) × number of tokens 
            # in the input file × number of epochs trained
            print(f"Fine-tuning cost: {status_response.hyperparameters.n_epochs * status_response.trained_tokens * COST[model_name] / 1_000_000}")
            return {"model_name": model_name}
        elif status == 'failed' or status == 'cancelled':
            print("Fine-tuning failed.")
            return {"error": "Fine-tuning failed."}
        elif time_elapsed > 3600:
            print("Fine-tuning took too long.")
            return {"error": "Fine-tuning took too long."}
        
        time.sleep(10)
        time_elapsed += 10

if __name__ == "__main__":
    dataset_path = "train_openai.jsonl"
    if not os.path.isfile(dataset_path):
        print(f"File {dataset_path} does not exist. Please provide a valid dataset file.")
    else:
        response = train(dataset_path)
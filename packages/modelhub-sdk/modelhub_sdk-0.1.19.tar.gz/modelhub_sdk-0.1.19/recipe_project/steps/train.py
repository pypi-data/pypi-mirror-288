# steps/train.py

import os
import pickle
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_diabetes
from sklearn.metrics import mean_squared_error, r2_score
from modelhub.client import ModelHub

load_dotenv()

# Initialize the ModelHub client
modelhub_client = ModelHub(base_url="https://api-modelhub.sprint.autonomize.dev")

# Get the MLflow client from ModelHub client
mlflow = modelhub_client.mlflow()

mlflow.set_experiment(experiment_id="9")

def train_and_log_model():
    # Load dataset
    diabetes = load_diabetes()
    X = diabetes.data
    y = diabetes.target

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize model
    model = LinearRegression()

    # Start an MLflow run
    with mlflow.start_run(run_name="train"):
        try:
            # Train the model
            model.fit(X_train, y_train)

            # Make predictions
            y_pred = model.predict(X_test)

            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            # Log parameters
            mlflow.log_param("random_state", 42)
            mlflow.log_param("test_size", 0.2)

            # Log metrics
            mlflow.log_metric("mse", mse)
            mlflow.log_metric("r2", r2)

            # Log model
            mlflow.sklearn.log_model(model, "model")

            print("Model training and logging complete")

        except Exception as e:
            print(f"An error occurred: {e}")
            mlflow.end_run(status=mlflow.entities.RunStatus.FAILED)
            raise

if __name__ == "__main__":
    train_and_log_model()
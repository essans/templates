#!/usr/bin/env python3

from pathlib import Path
import argparse
import yaml
from loguru import logger


def load_config(config_path: Path) -> dict:
    """Load configuration from a YAML file."""
    logger.info(f"Loading configuration from {config_path}")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def predict(input_data_path: Path, model_path: Path, predictions_dir: Path):
    """Simulate a prediction process."""
    logger.info(f"Using model from {model_path} to make predictions on {input_data_path}")
    predictions_dir.mkdir(parents=True, exist_ok=True)  # Ensure predictions directory exists

    # Simulate prediction process
    predictions = [0,1,1,0,1]
    output_path = predictions_dir / "predictions.csv"    

    logger.info(f"Saving predictions to {output_path}")

    # Example: pd.DataFrame(predictions).to_csv(output_path, index=False)
    logger.success("Predictions complete.")


def main():
    parser = argparse.ArgumentParser(description="Make predictions using a trained model.")
    parser.add_argument(
        "--config", type=Path, default="configs/config.yaml", help="Path to the configuration YAML file."
    )
    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Extract directories from configuration
    data_dir = Path(config["input_data"]["processed_dir"])
    model_dir = Path(config["model"]["model_dir"])
    predictions_dir = Path(config["outputs"]["predictions_dir"])

    # Construct specific paths
    input_data_path = data_dir / "test_features.csv"
    model_path = model_dir / "model.pkl"

    # Make predictions
    predict(input_data_path, model_path, predictions_dir)


if __name__ == "__main__":
    main()


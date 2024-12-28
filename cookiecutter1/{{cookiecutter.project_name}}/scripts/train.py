#!/usr/bin/env python3

from pathlib import Path
import argparse
import yaml
from loguru import logger
from tqdm import tqdm


def load_config(config_path: Path) -> dict:
    """Load configuration from a YAML file."""
    logger.info(f"Loading configuration from {config_path}")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def train_model(features_path: Path, labels_path: Path, model_path: Path, logs_dir: Path):
    """Simulate a model training process."""
    logger.info(f"Training model with features from {features_path} and labels from {labels_path}")
    logs_dir.mkdir(parents=True, exist_ok=True)

    for i in tqdm(range(10), desc="Training Progress"):
        if i == 5:
            logger.info("Simulating an event at iteration 5.")
    logger.success(f"Training complete. Model saved to {model_path}")


def main():
    parser = argparse.ArgumentParser(description="Train a machine learning model.")
    parser.add_argument(
        "--config", type=Path, default="configs/config.yaml", help="Path to the configuration YAML file.")
    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Extract directories from configuration
    data_dir = Path(config["input_data"]["processed_dir"])
    model_dir = Path(config["model"]["model_dir"])
    logs_dir = Path(config["outputs"]["logs_dir"])

    # Construct specific paths
    features_path = data_dir / "features.csv"
    labels_path = data_dir / "labels.csv"
    model_path = model_dir / "model.pkl"

    # Ensure requires directories exist
    for path in [data_dir, model_dir, logs_dir]:
        path.mkdir(parents=True, exist_ok=True)

    # Train the model
    train_model(features_path, labels_path, model_path, logs_dir)


if __name__ == "__main__":
    main()


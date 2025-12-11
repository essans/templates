import logging
import sys
from pathlib import Path
from typing import Union

import utils

PROJECT_ROOT = utils.get_project_root()

DEFAULT_LOG_FILE = PROJECT_ROOT / "outputs" / "logs" / "embeddings_lab1.log"
DEFAULT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def setup_logging(
    log_file_path: Union[str, Path] = DEFAULT_LOG_FILE,
    log_to_screen: bool = True,
    log_level: int = logging.INFO,
    ) -> None:
    
    """
    Configure the root logger with a file handler and optional screen handler.
    Every call resets handlers, so changes take effect immediately.
    """
    root = logging.getLogger()

    # Remove any existing handlers (including Jupyter's defaults)
    for h in root.handlers[:]:
        root.removeHandler(h)

    log_file_path = Path(log_file_path)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    formatter.default_msec_format = '%s.%03d'

    # File handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    root.addHandler(file_handler)

    # Optional screen handler
    if log_to_screen:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(log_level)
        root.addHandler(stream_handler)

    root.setLevel(log_level)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

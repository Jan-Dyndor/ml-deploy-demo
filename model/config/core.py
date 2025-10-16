from pydantic import BaseModel
from typing import List
from pathlib import Path
import model
from strictyaml import YAML, load

PACKAGE_ROOT = Path(model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"


class ModelConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering.
    """
    random_state: int
    test_size: float
    selected_features = List[str]
    target: str

def find_config_file() -> Path:
    """Locate configuration file"""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Configuration file not found: {CONFIG_FILE_PATH}")

def fetch_config_file_from_yaml(cfg_file_path: Path | None) -> YAML:
    if not cfg_file_path:
        cfg_file_path = find_config_file()

    if cfg_file_path:
        with open(cfg_file_path, "r") as cfg_file:
            parse_config = load(cfg_file.read())
            return parse_config
    raise OSError(f"Configuration file not found: {cfg_file_path}")

def create_and_validate_config(parsed_congif: YAML | None) -> ModelConfig:
    if not parsed_congif:
        parsed_congif = fetch_config_file_from_yaml()

    _config = ModelConfig(**parsed_congif)
    return _config

config = create_and_validate_config()
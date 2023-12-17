import json
import os

from pydantic import BaseModel

DEFAULT_MODEL = "lama"
AVAILABLE_MODELS = ["lama"]
AVAILABLE_DEVICES = ["cuda", "cpu"]
DEFAULT_DEVICE = "cpu"

DEFAULT_MODEL_DIR = os.getenv(
    "XDG_CACHE_HOME", os.path.join(os.path.expanduser("~"), ".cache")
)


class Config(BaseModel):
    model: str = DEFAULT_MODEL
    device: str = DEFAULT_DEVICE
    model_dir: str = DEFAULT_MODEL_DIR
    input: str = None
    output_dir: str = None

def load_config(installer_config: str):
    if os.path.exists(installer_config):
        with open(installer_config, "r", encoding="utf-8") as f:
            return Config(**json.load(f))
    else:
        return Config()

import os
from models import Config
import json

scripts_dir = os.getenv("SCRIPTS_DIR")
config = Config.model_validate_json(open("config.json", "r").read())
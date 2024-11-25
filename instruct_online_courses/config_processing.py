import importlib.resources
import logging

from dynaconf import Dynaconf

# Config parameters
with importlib.resources.as_file(importlib.resources.files("instruct_online_courses")) as config_path:
    settings = Dynaconf(settings_files=[config_path / "settings.toml", config_path / ".secrets.toml"])

# Logging
logger = logging.getLogger("instruct_online_courses")
logger.setLevel(settings.LOG_LEVEL.upper())
handler = logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter("%(levelname)s [%(asctime)s]: %(message)s")
handler.setFormatter(formatter)

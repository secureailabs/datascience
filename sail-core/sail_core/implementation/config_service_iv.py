import json
import os
from typing import Dict

from sail_core.api.config_service_base import ConfigServiceBase


class ConficServiceIv(ConfigServiceBase):
    def __init__(self) -> None:
        self.__config: Dict

    def initialize(self) -> None:
        IV_SETTINGS_FILE = "/app/datascience/InitializationVector.json"

        if os.environ.get("IV_FILEPATH") is not None:
            IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")

        with open(IV_SETTINGS_FILE) as initial_settings:
            self.__config = json.load(initial_settings)

    def get_config(self) -> Dict:
        return self.__config.copy()

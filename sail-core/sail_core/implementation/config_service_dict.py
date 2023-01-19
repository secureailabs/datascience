from typing import Dict

from sail_core.api.config_service_base import ConfigServiceBase


class ConficServiceDict(ConfigServiceBase):
    def __init__(self, config: Dict) -> None:
        self.__config = config.copy()

    def initialize(self) -> None:
        pass

    def get_config(self) -> Dict:
        return self.__config.copy()

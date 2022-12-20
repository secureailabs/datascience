from typing import Dict

from sail_core.api.config_service_base import ConfigServiceBase
from sail_core.implementation_manager import ImplementationMaganger


class ConficServiceDict(ConfigServiceBase):
    def __init__(self, config: Dict) -> None:
        self.__config = config.copy()

    def initialize(self, implementation_manager: ImplementationMaganger) -> None:
        pass

    def get_config(self) -> Dict:
        return self.__config.copy()

from abc import abstractmethod
from typing import Dict

from sail_core.api.service_base import ServiceBase


class ConfigServiceBase(ServiceBase):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_config(self) -> Dict:
        raise NotImplementedError()

from abc import abstractmethod
from typing import Dict

from sail_core.api.service_base import ServiceBase


class ComputeClientSeriviceBase(ServiceBase):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def log(self, logstring: str) -> Dict:
        raise NotImplementedError()

from abc import abstractmethod
from typing import Dict

from sail_core.api.service_base import ServiceBase


class LoggingServiceBase(ServiceBase):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def reference_to_object(self, reference_id: str) -> object:
        raise NotImplementedError()

    @abstractmethod
    def object_to_reference(self, object: str) -> str:
        raise NotImplementedError()

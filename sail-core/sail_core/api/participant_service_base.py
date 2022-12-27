from abc import abstractmethod

from sail_core.api.service_base import ServiceBase


class LoggingServiceBase(ServiceBase):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def call(self, dataset_id, logstring: str) -> None:
        raise NotImplementedError()

from abc import ABC, abstractmethod


class ServiceBase(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError()

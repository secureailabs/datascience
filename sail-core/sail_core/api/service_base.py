from abc import ABC, abstractmethod
from typing import Dict


class ServiceBase(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def initialize(self) -> None:
        raise NotImplementedError()

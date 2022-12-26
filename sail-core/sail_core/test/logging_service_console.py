from sail_core.api.logging_service_base import LoggingServiceBase
from sail_core.implementation_manager import ImplementationMaganger


class LoggingServiceConsole(LoggingServiceBase):
    def __init__(self) -> None:
        pass

    def initialize(self, implementation_manager: ImplementationMaganger) -> None:
        pass

    def log(self, logstring: str) -> None:
        print(logstring, flush=True)

from sail_core.api.logging_service_base import LoggingServiceBase


class LoggingServicePrint(LoggingServiceBase):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self) -> None:
        pass

    def log(self, logstring: str) -> None:
        print(logstring, flush=True)

from typing import Optional

from sail_core.api.config_service_base import ConfigServiceBase
from sail_core.api.logging_service_base import LoggingServiceBase
from sail_core.api.participant_service_base import ParticipantServiceBase


class ImplementationManager:
    _instance: "ImplementationManager"

    def __init__(self) -> None:
        self.__logging_service: Optional[LoggingServiceBase] = None
        self.__config_service: Optional[ConfigServiceBase] = None
        self.__participant_service: Optional[ParticipantServiceBase] = None
        self.__is_initialized = False

    @property
    def is_initialized(self) -> bool:
        return self.__is_initialized

    def __call__(self):
        raise TypeError("Singletons must be accessed through `get_instance()`.")

    @staticmethod
    def get_instance() -> "ImplementationManager":
        try:
            return ImplementationManager._instance

        except AttributeError:
            ImplementationManager._instance = ImplementationManager()
            return ImplementationManager._instance

        """
        the initialize function serves to give the seriveces an opportunity to use eachother before the get used themselves.
        For instance the can use the config service to get their configuation, or the platform service to establish some metadata about the provisioning
        """

    def initialize(self):
        if self.__is_initialized:
            raise RuntimeError("can only initialize once")
        self.__is_initialized = True

        if self.__logging_service is not None:
            self.__logging_service.initialize()
        if self.__config_service is not None:
            self.__config_service.initialize()
        if self.__participant_service is not None:
            self.__participant_service.initialize()

    def get_logging_service(self) -> LoggingServiceBase:
        if not self.__is_initialized:
            raise RuntimeError("Implementation Manager is not initialized")
        return self.__logging_service

    def set_logging_service(self, logging_service: LoggingServiceBase) -> None:
        if self.__is_initialized:
            raise RuntimeError("Cannot change implemention: Implementation Manager is initialized")
        self.__logging_service = logging_service

    def get_config_service(self) -> ConfigServiceBase:
        if not self.__is_initialized:
            raise RuntimeError("Implementation Manager is not initialized")
        return self.__config_service

    def set_config_service(self, config_service: ConfigServiceBase) -> None:
        if self.__is_initialized:
            raise RuntimeError("Cannot change implemention: Implementation Manager is initialized")
        self.__config_service = config_service

    def get_participant_service(self) -> ParticipantServiceBase:
        if not self.__is_initialized:
            raise RuntimeError("Implementation Manager is not initialized")
        return self.__participant_service

    def set_participant_service(self, participant_service: ParticipantServiceBase) -> None:
        if self.__is_initialized:
            raise RuntimeError("Cannot change implemention: Implementation Manager is initialized")
        self.__participant_service = participant_service

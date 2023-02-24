import os
from typing import Dict

import requests
from sail_core.api.config_service_base import ConfigServiceBase
from sail_core.implementation_manager import ImplementationManager


class ConfigServiceClient(ConfigServiceBase):
    def __init__(self) -> None:
        self.__config: Dict

    def initialize(self, implementation_manager: ImplementationManager) -> None:
        # config = implementation_manager.get_config_service()
        # url = config["config_service"]["url_server_config"]
        # TODO something magic here has to happen to get the config secret, somthing with
        config_secret = "XXX"
        payload = {"config_secret": config_secret}
        url_config_server = os.environ["URL_CONFIG_SERVER"]
        response = requests.get(url_config_server, data=payload)
        if response.status_code != 200:
            raise RuntimeError("Config Service could not initialize, config server request failed")
        self.__config = response.json()

    def get_config(self) -> Dict:
        return self.__config.copy()

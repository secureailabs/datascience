from sail_core.implementation.config_service_dict import ConficServiceDict
from sail_core.implementation.config_service_iv import ConficServiceIv
from sail_core.implementation.logging_service_print import LoggingServicePrint
from sail_core.implementation_manager import ImplementationManager

# config_service = ConficServiceIv()
# logging_service = LoggingServicePrint()
# imlementation_manager = ImplementationManager.get_instance()
# imlementation_manager.set_config_service(config_service)
# imlementation_manager.set_logging_service(logging_service)
# imlementation_manager.initialize()

config_service = ConficServiceDict({"a": 1, "b": 2})
logging_service = LoggingServicePrint()
imlementation_manager = ImplementationManager.get_instance()
imlementation_manager.set_config_service(config_service)
imlementation_manager.set_logging_service(logging_service)
imlementation_manager.initialize()


def run_program():
    imlementation_manager = ImplementationManager.get_instance()
    config_service = imlementation_manager.get_config_service()
    logging_service = imlementation_manager.get_logging_service()
    logging_service.log(str(config_service.get_config()))


run_program()

import json
import logging
import os
import threading

from fastapi import Body, Depends, FastAPI, HTTPException, Path, Response, status
from fastapi.responses import RedirectResponse
from log.audit_log import _AsyncLogger, log_message
from sail_safe_functions.aggregator import preprocessing, statistics, visualization
from sail_safe_functions.aggregator.client_rpc_zero import ClientRPCZero
from sail_safe_functions.test.helper_sail_safe_functions.participant_service_local import ParticipantSeriviceLocal
from sail_safe_functions.test.helper_sail_safe_functions.test_service_reference import TestServiceReference
import config

# TODO make this a other implementation that autoconfigures
# participant_service = ParticipantServiceClientDict()
# for dataset_id, scn_name, scn_port in zip(list_dataset_id, scn_names, scn_ports):
#     participant_service.register_client(dataset_id, ClientRPCZero(scn_name, scn_port))
#     print(f"Connected to SCN {scn_name} serving dataset {dataset_id}")


# implementation_manager = ImplementationManager.get_instance()
# implementation_manager.set_participant_service(participant_service)
# implementation_manager.initialize()

# implementation_manager = ImplementationManager.get_instance()
# implementation_manager.set_participant_service(ParticipantSeriviceLocal())
# implementation_manager.initialize()

from fastapi import APIRouter

router = APIRouter(
    prefix='/aggregator',
    tags = ['base_functionality']
)

# dataframe_name_lookup = {}

# scn_names = []
# scn_ports = []
# list_dataset_id = []
# IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")

# if os.environ.get("IV_FILEPATH") is not None:
#     IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")

# with open(IV_SETTINGS_FILE) as initial_settings:
#     configuration = json.load(initial_settings)
#     for entry in configuration["secure_computation_nodes"]:
#         scn_names.append(entry["ip_address"])
#         scn_ports.append(5556)
#         list_dataset_id.append(entry["dataset_id"])
# service_reference = TestServiceReference.get_instance()


class Audit_log_task(threading.Thread):
    """
    Auxillary class for audit log server in isolated thread
    """

    def run(self):
        """
        Start async logger server
        """
        _AsyncLogger.start_log_poller(_AsyncLogger.ipc, _AsyncLogger.port)


@router.on_event("startup")
async def start_audit_logger():
    """
    Start async audit logger server at start up as a background task
    """
    t = Audit_log_task()
    t.start()


async def log_validation_failure(message):
    logger = logging.getLogger("uvicorn.error")
    logger.error(message)
    await log_message(message)


def query_limit_n(series, n=0) -> bool:
    """
    Checks data or series in question is over a given threshold.

    :param: data: the data item being checked
    :type: remote dataframe or remote series
    :return: True or False relating to whether the threshold has been surpassed
    :type: Boolean
    """
    return statistics.count(series) > n


async def validate(series):
    """
    Validates execution criteria for data inputs
    :param: data: the data item being validated
    :type: Remote Dataframe or Remote Series
    :return: None
    :type: None
    """
    if not query_limit_n(series):
        message = "Validation Failure: Sample size too small"
        await log_validation_failure(message)
        raise HTTPException(status_code=500, detail=message)
    else:
        return

    # CHECKS
    # TODO:
    #       1. Check for pandas query injection in column_id string
    # CLOSE CHECKS


# OUTLAWED METHODS - Returns raw data
# def get_series(series_uuid: str):
#     return service_reference.reference_to_federated_series(series_uuid)


# def get_dataframe(dataframe_uuid: str):
#     return service_reference.reference_to_federated_dataframe(dataframe_uuid)
# END OUTLAWED METHODS


# Redirect Response Breaks things + we dont need this?
# @app.post(
#     path="/",
#     description="Returns Swagger Docs",
#     response_description="Redirect response brings user to the docs page.",
#     response_model=RedirectResponse,
#     response_model_by_alias=False,
#     response_model_exclude_unset=True,
#     dependencies=None,
#     status_code=status.HTTP_200_OK,
#     operation_id="get_docs",
# )
# @app.get("/")
# async def root():
#     """
#     Redirects user to docs as hompage
#     """
#     return RedirectResponse("/docs")




# START VISUALIZATION
@router.post(
    path="/visualization_histogram",
    description="Creates a histogram of a given Series.",
    response_description="The Histogram of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="visualization_histogram",
)
async def histogram_federated(
    series_1_id: str = Body(description="The identifier of the Series"),
    bin_count: int = Body(description="How many bins to sort the Series into."),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)

    await validate(series_1)

    figure = visualization.histogram_federated(series_1, bin_count)

    return {"figure": figure}


@router.post(
    path="/visualization_kernel_density_estimation",
    description="Creates a Kernel Density Estimation of a given Series.",
    response_description="The Kernel Density Estimation of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="visualization_kernel_density_estimation",
)
async def kernel_density_estimation(
    series_1_id: str = Body(description="The identifier of the Series"),
    bin_size: float = Body(description="The size of each bin the Serirs will be sorted into."),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)

    await validate(series_1)

    figure = visualization.kernel_density_estimation(series_1, bin_size)

    return {"figure": figure}
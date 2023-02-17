import json
import os

import config
from config import validate
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, Path, Response, status
from sail_safe_functions.aggregator import visualization
from sail_safe_functions.test.helper_sail_safe_functions.test_service_reference import TestServiceReference

# from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
# from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
# from sail_safe_functions.aggregator.data_model.data_model_tabular import DataModelTabular

# TODO: take this out and make it globally accessible
scn_names = []
scn_ports = []
list_dataset_id = []
IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")
service_reference = TestServiceReference.get_instance()

if os.environ.get("IV_FILEPATH") is not None:
    IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")

with open(IV_SETTINGS_FILE) as initial_settings:
    configuration = json.load(initial_settings)
    for entry in configuration["secure_computation_nodes"]:
        scn_names.append(entry["ip_address"])
        scn_ports.append(5556)
        list_dataset_id.append(entry["dataset_id"])
# TODO: take this out and make it globally accessible


router = APIRouter(
    prefix="/visualisation",
)


@router.post(
    path="/histogram",
    description="Creates a histogram of a given Series.",
    response_description="The Histogram of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="histogram",
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
    path="/kernel_density_estimation",
    description="Creates a Kernel Density Estimation of a given Series.",
    response_description="The Kernel Density Estimation of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="kernel_density_estimation",
)
async def kernel_density_estimation(
    series_1_id: str = Body(description="The identifier of the Series"),
    bin_size: float = Body(description="The size of each bin the Serirs will be sorted into."),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)

    await validate(series_1)

    figure = visualization.kernel_density_estimation(series_1, bin_size)

    return {"figure": figure}

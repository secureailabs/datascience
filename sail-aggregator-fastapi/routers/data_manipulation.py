
from fastapi import Body, Depends, FastAPI, HTTPException, Path, Response, status
from fastapi import APIRouter
from sail_safe_functions.test.helper_sail_safe_functions.test_service_reference import TestServiceReference
import config
import os
import json

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
    prefix='/data_manipulation',
)


@router.post(
    path="/data_frame_tabular_select_dataframe.",
    description="Select an individual datafame from a tabular dataframe.",
    response_description="Reference to Dataframe.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="data_frame_tabular_select_dataframe",
)
async def data_frame_tabular_select_dataframe(
    data_frame_tabular_id: str = Body(description="The identifier of the dataframe being queried."),
    data_frame_name: str = Body(description="The name of the dataframe being pulled from the tabular dataframe."),
) -> dict:
    data_frame_tabular = service_reference.get_instance().reference_to_data_set_tabular(data_frame_tabular_id)
    data_frame = data_frame_tabular[data_frame_name]

    data_frame_id = service_reference.get_instance().federated_dataframe_to_reference(data_frame)
    return {"data_frame_id": data_frame_id}


@router.post(
    path="/data_frame_select_series.",
    description="Select an individual series from a  dataframe.",
    response_description="Reference to Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="data_frame_select_series",
)
async def data_frame_select_series(
    data_frame_id: str = Body(description="The identifier of the dataframe being queried."),
    series_name: str = Body(description="The name of the seires to be pulled from the dataframe."),
) -> dict:
    data_frame = service_reference.get_instance().reference_to_federated_dataframe(data_frame_id)
    series = data_frame[series_name]

    series_id = service_reference.get_instance().federated_series_to_reference(series)
    return {"series_id": series_id}
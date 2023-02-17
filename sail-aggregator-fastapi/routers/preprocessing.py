import json
import os

import config
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, Path, Response, status
from sail_safe_functions.aggregator import preprocessing
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
    prefix="/preprocessing",
)

# Doesn't work but we should allow it
# @router.post("/preprocessing/series/drop_missing/{series_id}")
# async def series_drop_missing(series_id: str) -> dict:
#     orig_series = service_reference.get_instance().reference_to_federated_series(
#         series_id
#     )
#     new_series = preprocessing.drop_missing(
#         orig_series, axis=0, how="any", thresh=None, subset=None
#     )

#     new_series_id = service_reference.get_instance().federated_series_to_reference(
#         new_series
#     )

#     return {"series_id": new_series_id}


@router.post(
    path="/dataframe_drop_missing.",
    description="Drop all missing values from a dataframe and return this copy.",
    response_description="Reference to cleaned dataframe.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="dataframe_drop_missing",
)
async def dataframe_drop_missing(
    dataset_id: str = Body(description="Identifier of the dataframe to be cleaned."),
) -> dict:
    orig_data_frame = service_reference.get_instance().reference_to_federated_dataframe(dataset_id)
    new_data_frame = preprocessing.drop_missing(orig_data_frame, axis=0, how="any", thresh=None, subset=None)

    new_data_frame_id = service_reference.get_instance().federated_dataframe_to_reference(new_data_frame)

    return {"new_data_frame_id": new_data_frame_id}


@router.post(
    path="/data_frame_query.",
    description="Query a Dataframe for a given String.",
    response_description="Reference to result of dataframe query.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="data_frame_query",
)
async def data_frame_query(
    data_frame_id: str = Body(description="The identifier of the dataframe to be queried."),
    query_str: str = Body(description="The string to be queried."),
) -> dict:
    orig_data_frame = service_reference.get_instance().reference_to_federated_dataframe(data_frame_id)
    new_data_frame = preprocessing.query(orig_data_frame, query_str)

    new_data_frame_id = service_reference.get_instance().federated_dataframe_to_reference(new_data_frame)

    return {"result_data_frame_id": new_data_frame_id}


from fastapi import Body, Depends, FastAPI, HTTPException, Path, Response, status
from fastapi import APIRouter
from sail_safe_functions.test.helper_sail_safe_functions.test_service_reference import TestServiceReference
from pydantic import BaseModel
from typing import List
from sail_safe_functions.aggregator import preprocessing
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
    prefix='/data_ingestion',
)


class DataFederation(BaseModel):
    list_dataset_id: List[str]


# DATA INGESTION
@router.post(
    path="/read_longitudinal_fhirv1",
    description="Reads a Longitudinal dataset from a fhirv1 data source.",
    response_description="Reference to Longitudinal Dataframe model.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="read_longitudinal_fhirv1",
)
async def read_longitudinal_fhirv1() -> dict:
    dataset_longitudinal = preprocessing.read_dataset_fhirv1(list_dataset_id)

    longitudinal_id = service_reference.get_instance().federated_longitudinal_data_to_reference(dataset_longitudinal)

    return {"longitudinal_id": longitudinal_id}


@router.post(
    path="/read_dataset_tabular_from_longitudinal",
    description="Populates a Tabular dataset from a Longitudinal dataset.",
    response_description="Reference to Tabular Dataframe.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="read_dataset_tabular_from_longitudinal",
)
async def read_dataset_tabular_from_longitudinal(
    longitudinal_id: str = Body(description="The identifier of the Longitudinal Dataset to be added from."),
    dataset_federation_id: str = Body(description="The identifier of the dataset federation"),
    dataset_federation_name: str = Body(description="The name of the federation being worked with."),
    data_model_tabular_id: str = Body(
        description="the identifier of the data model being used to query from the longitudinal dataset."
    ),
) -> dict:
    dataset_longitudinal = service_reference.get_instance().reference_to_federated_longitudinal_data(longitudinal_id)
    data_model_tablular = service_reference.get_instance().reference_to_data_model_tabular(data_model_tabular_id)
    dataset_tabular = preprocessing.convert_to_dataset_tabular(
        dataset_longitudinal,
        dataset_federation_id,
        dataset_federation_name,
        data_model_tablular,
    )

    dataset_id = service_reference.get_instance().data_set_tabular_to_reference(dataset_tabular)

    return {"dataset_id": dataset_id}


# TODO: add 'read' to operation_id
@router.post(
    path="/dataset_tabular_fhirv1",
    description="Pull data from fhirv1 source straight to tabular Dataframe.",
    response_description="Reference to Tabular Dataframe.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="dataset_tabular_fhirv1",
)
async def dataset_tabular_fhirv1(
    dataset_federation_id: str = Body(description="The identifier of the data federation"),
    dataset_federation_name: str = Body(description="the name of the data federation"),
    data_model_tabular_id: str = Body(
        description="The identifier of the tabular dataframe modle being used to pull data from the fhirv1 source."
    ),
) -> dict:
    dataset_longitudinal = preprocessing.read_dataset_fhirv1(list_dataset_id)
    data_model_tablular = service_reference.get_instance().reference_to_data_model_tabular(data_model_tabular_id)

    dataframe_tabular = preprocessing.convert_to_dataset_tabular(
        dataset_longitudinal,
        dataset_federation_id,
        dataset_federation_name,
        data_model_tablular,
    )

    tabular_dataframe_id = service_reference.get_instance().data_set_tabular_to_reference(dataframe_tabular)

    return {"tabular_dataframe_id": tabular_dataframe_id}


@router.post(
    path="/read_tabular_dataframe_csvv1",
    description="Pull a Tabular Dataframe from csvv1 source.",
    response_description="Reference to Tabular Dataframe.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="read_tabular_dataframe_csvv1",
)
async def read_tabular_dataframe_csvv1(
    data_federation: DataFederation = Body(description="TODO: What is this datatype? This should be a reference"),
) -> dict:
    list_dataset_id = data_federation.list_dataset_id
    dataset_tabular = preprocessing.read_dataset_csvv1(list_dataset_id)
    dataset_id = service_reference.get_instance().data_set_tabular_to_reference(dataset_tabular)
    return {"dataset_id": dataset_id}
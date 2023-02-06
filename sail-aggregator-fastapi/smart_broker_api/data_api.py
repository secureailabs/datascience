from typing import List

import requests
from fast_api_client.models import (
    BodyDataFrameSelectSeries,
    BodyDataFrameTabularSelectDataframe,
    BodyDatasetTabularFhirv1,
    BodyReadDatasetTabularFromLongitudinal,
    DataFederation,
)


def read_longitudinal_fhirv1(operation):

    return operation.read_longitudinal_fhirv1().additional_properties["longitudinal_id"]


def read_dataset_tabular_from_longitudinal(
    operation,
    longitudinal_id,
    dataset_federation_id,
    dataset_federation_name,
    data_model_tabular_id,
):

    body = BodyReadDatasetTabularFromLongitudinal(
        longitudinal_id, dataset_federation_id, dataset_federation_name, data_model_tabular_id
    )

    return operation.read_dataset_tabular_from_longitudinal(body).additional_properties["dataset_id"]


# TODO: add 'read' to operation_id
def dataset_tabular_fhirv1(operation, dataset_federation_id, dataset_federation_name, data_model_tabular_id):

    body = BodyDatasetTabularFhirv1(dataset_federation_id, dataset_federation_name, data_model_tabular_id)

    return operation.dataset_tabular_fhirv1(body).additional_properties["tabular_dataframe_id"]


def data_frame_tabular_select_data_frame(operation, data_frame_tabular_id, data_frame_name):

    body = BodyDataFrameTabularSelectDataframe(data_frame_tabular_id, data_frame_name)

    return operation.data_frame_tabular_select_dataframe(body).additional_properties["data_frame_id"]


def data_frame_select_series(operation, data_frame_id, series_name):

    body = BodyDataFrameSelectSeries(data_frame_id, series_name)

    return operation.data_frame_select_series(body).additional_properties["series_id"]


def read_tabular_dataframe_csvv1(operation, list_dataset_id: List[str]):

    body = DataFederation(list_dataset_id)

    return operation.read_tabular_dataframe_csvv1(body)["dataset_id"]

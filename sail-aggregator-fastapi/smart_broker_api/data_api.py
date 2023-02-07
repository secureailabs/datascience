from typing import List

from fast_api_client.models import (
    BodyDataFrameSelectSeries,
    BodyDataFrameTabularSelectDataframe,
    BodyDatasetTabularFhirv1,
    BodyReadDatasetTabularFromLongitudinal,
    DataFederation,
)
from fast_api_client.sail_class import SyncOperations


def read_longitudinal_fhirv1(operation: SyncOperations) -> str:
    """
    Reads Longitudinal Dataset from FHIRv1 source on remote SCNs.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations

    Returns
    -------
    string
       The identifier of the newlygenerated Longitudinal Dataframe.
    """
    return operation.read_longitudinal_fhirv1().additional_properties["longitudinal_id"]


def read_dataset_tabular_from_longitudinal(
    operation: SyncOperations,
    longitudinal_id: str,
    dataset_federation_id: str,
    dataset_federation_name: str,
    data_model_tabular_id: str,
) -> str:
    """
    Transforms a Longitudinal Dataset into Tabular form, given a valid Tabular model.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param longitudinal_id: The identifier of the Longitudinal Dataset
    :type longitudinal_id: string
    :param dataset_federation_id: The identifier of the federation to which the Longitudinal Dataset belongs
    :type dataset_federation_id: string
    :param dataset_federation_name: The name of the federation to which the Longitudinal Dataset belongs
    :type dataset_federation_name: string
    :param data_model_tabular_id: The identifier of the Tabular Data Model which pulls values from the Longitudinal Dataset.
    :type data_model_tabular_id: string

    Returns
    -------
    string
       The identifier of the newly generated Tabular Dataframe.
    """
    body = BodyReadDatasetTabularFromLongitudinal(
        longitudinal_id, dataset_federation_id, dataset_federation_name, data_model_tabular_id
    )

    return operation.read_dataset_tabular_from_longitudinal(body).additional_properties["dataset_id"]


# TODO: add 'read' to operation_id
def dataset_tabular_fhirv1(
    operation: SyncOperations, dataset_federation_id: str, dataset_federation_name: str, data_model_tabular_id: str
):
    """
    Reads Tabular Dataset from FHIRv1 source on remote SCNs.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param dataset_federation_id: The identifier of the federation to which the Longitudinal Dataset belongs
    :type dataset_federation_id: string
    :param dataset_federation_name: The name of the federation to which the Longitudinal Dataset belongs
    :type dataset_federation_name: string
    :param data_model_tabular_id: The identifier of the Tabular Data Model which pulls values from the Longitudinal Dataset.
    :type data_model_tabular_id: string

    Returns
    -------
    string
       The identifier of the newly generated Tabular Dataframe.
    """
    body = BodyDatasetTabularFhirv1(dataset_federation_id, dataset_federation_name, data_model_tabular_id)

    return operation.dataset_tabular_fhirv1(body).additional_properties["tabular_dataframe_id"]


def data_frame_tabular_select_data_frame(
    operation: SyncOperations, data_frame_tabular_id: str, data_frame_name: str
) -> str:
    """
    Selects Dataframe from Tabular Dataframe
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param data_frame_tabular_id: The identifier of the Tabular Dataframe to pull the Dataframe from
    :type data_frame_tabular_id: string
    :param data_frame_name: The name of the dataframe to be pulled
    :type data_frame_name: string

    Returns
    -------
    string
       The identifier of the pulled Dataframe.
    """

    body = BodyDataFrameTabularSelectDataframe(data_frame_tabular_id, data_frame_name)

    return operation.data_frame_tabular_select_dataframe(body).additional_properties["data_frame_id"]


def data_frame_select_series(operation: SyncOperations, data_frame_id: str, series_name: str) -> str:
    """
    Selects Series from Dataframe
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param data_frame_id: The identifier of the Tabular Dataframe to pull the Dataframe from
    :type data_frame_id: string
    :param series_name: The name of the dataframe to be pulled
    :type series_name: string

    Returns
    -------
    string
       The identifier of the pulled Dataframe.
    """

    body = BodyDataFrameSelectSeries(data_frame_id, series_name)

    return operation.data_frame_select_series(body).additional_properties["series_id"]


def read_tabular_dataframe_csvv1(operation: SyncOperations, list_dataset_id: List[str]) -> str:
    """
    Reads a Tabular Dataframe from csvv1 source
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param list_dataset_id: The identifiers of the csv1 type dataset to be pulled from.
    :type list_dataset_id: string

    Returns
    -------
    string
       The identifier of the pulled Tabular Dataframe.
    """

    body = DataFederation(list_dataset_id)

    return operation.read_tabular_dataframe_csvv1(body)["dataset_id"]

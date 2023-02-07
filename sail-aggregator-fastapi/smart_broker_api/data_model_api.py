from fast_api_client.models import (
    BodyDataframeModelAddNewSeriesModel,
    BodyNewSeriesModelNumerical,
    BodyTabularModelAddDataframeModel,
)
from fast_api_client.sail_class import SyncOperations


def new_data_model_data_frame(operation: SyncOperations, data_frame_name: str) -> str:
    """
    Creates a new Dataframe model.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param data_frame_name: Name of the Dataframe to be created
    :type series_1_id: string

    Returns
    -------
    string
       The identifier of the newly created Dataframe model.
    """
    return operation.new_data_model_data_frame(data_frame_name).additional_properties["data_model_id"]


def new_tabular_model(operation: SyncOperations) -> str:
    """
    Creates a new Tabular Dataframe model.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations

    Returns
    -------
    string
       The identifier of the newly created Tabular Dataframe model.
    """
    return operation.new_tabular_model().additional_properties["data_frame_tabular_id"]


# TODO: enumerate valid type aggregator for docs
def new_series_model_numerical(
    operation: SyncOperations, series_name: str, measurement_source_name: str, type_aggregator: str, unit: str
):
    """
    Creates a new numerical Series model.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param series_name: Name of the new Series model
    :type series_name: string
    :param measurement_source_name: Source field to populate the corresponding Series with.
    :type measurement_source_name: string
    :param type_aggregator: The type of aggregator to use to populate the Series
    :type type_aggregator: string
    :param unit: The unit of measurement used in the Series
    :type unit: string

    Returns
    -------
    string
       The identifier of the newly created numerical Series model.
    """
    body = BodyNewSeriesModelNumerical(series_name, measurement_source_name, type_aggregator, unit)
    # TODO: change series to series_id
    return operation.new_series_model_numerical(body).additional_properties["series"]


# TODO: enumerate valid type aggregator for docs
def data_frame_add_series(
    operation: SyncOperations, dataframe_model_id, series_name, measurement_source_name, type_agregator, unit
):
    """
    Creates a new numerical Series model and adds it to a dataframe model.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param dataframe_model_id: The identifier of the dataframe to be added to
    :type dataframe_model_id: string
    :param series_name: Name of the new Series model
    :type series_name: string
    :param measurement_source_name: Source field to populate the corresponding Series with.
    :type measurement_source_name: string
    :param type_aggregator: The type of aggregator to use to populate the Series
    :type type_aggregator: string
    :param unit: The unit of measurement used in the Series
    :type unit: string

    Returns
    -------
    string
       The identifier of the newly created numerical Series model.
    """
    body = BodyDataframeModelAddNewSeriesModel(
        dataframe_model_id, series_name, measurement_source_name, type_agregator, unit
    )

    return operation.dataframe_model_add_new_series_model(body).additional_properties["data_model_id"]


def tabular_model_add_dataframe_model(
    operation: SyncOperations, data_model_tabular_id: str, data_model_dataframe_id: str
) -> str:
    """
    Creates a new numerical Series model and adds it to a dataframe model.
    Parameters
    ----------
    :param operation: Object used to reference fast_api_client function calls
    :type operation: SyncOperations
    :param data_model_tabular_id: The identifier of the Tabular Dataframe Model to be added to
    :type data_model_tabular_id: string
    :param data_model_dataframe_id: The identifier of the Dataframe Model to be added to the Tabular Dataframe Model
    :type data_model_dataframe_id: string

    Returns
    -------
    string
       The identifier of the Tabular Dataframe model which was added to.
    """
    body = BodyTabularModelAddDataframeModel(data_model_tabular_id, data_model_dataframe_id)
    return operation.tabular_model_add_dataframe_model(body).additional_properties["data_frame_tabular_id"]

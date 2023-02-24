from sail_aggregator_client.models import BodyDataFrameQuery
from sail_aggregator_client.sail_class import SyncOperations


def dataframe_drop_missing(operation: SyncOperations, data_frame_id: str) -> str:
    """
    Remove missing values.
    Parameters
    ----------
    :param operation: Object used to reference sail_aggregator_client function calls
    :type operation: SyncOperations
    :param series_1_id: The id of the dataframe to drop values from
    :type series_1_id: string

    Returns
    -------
    str
        The id of the dataframe with missing values removed.
    """
    return operation.dataframe_drop_missing(data_frame_id).additional_properties["new_data_frame_id"]


def data_frame_query(operation: SyncOperations, data_frame_id: str, query: str) -> str:
    """
    Federated equivalent of (pd.DataFrame.query)
    Parameters
    ----------
    :param operation: Object used to reference sail_aggregator_client function calls
    :type operation: SyncOperations
    :param data_frame_id: The id of the dataframe to query
    :type series_1_id: string
    :param query: The query to be performed
    :type query: string

    Returns
    -------
    str
        The id of the resultant dataframe from the query.
    """

    body = BodyDataFrameQuery(data_frame_id, query)

    return operation.data_frame_query(body).additional_properties["result_data_frame_id"]


# NOTE: Doesn't work but we should allow it
# def drop_na_series(session, series_id):
#     payload = {"series_id": series_id}
#     result = requests.post(
#         "http://"
#         + session.ip
#         + ":"
#         + session.port
#         + "/preprocessing/series/drop_missing/"
#         + series_id,
#         params=payload,
#     )
#     return result.json()["series_id"]

import json
import logging
import os
import threading
from typing import List

from fastapi import Body, Depends, FastAPI, HTTPException, Path, Response, status
from fastapi.responses import RedirectResponse
from log.audit_log import _AsyncLogger, log_message
from pydantic import BaseModel
from sail_core.implementation.participant_service_client_dict import ParticipantServiceClientDict
from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.aggregator import preprocessing, statistics, visualization
from sail_safe_functions.aggregator.client_rpc_zero import ClientRPCZero
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions.test.helper_sail_safe_functions.participant_service_local import ParticipantSeriviceLocal
from sail_safe_functions.test.helper_sail_safe_functions.test_service_reference import TestServiceReference

app = FastAPI()

service_reference = TestServiceReference.get_instance()

dataframe_name_lookup = {}

scn_names = []
scn_ports = []
list_dataset_id = []
IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")


# if os.environ.get("IV_FILEPATH") is not None:
#     IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")

with open(IV_SETTINGS_FILE) as initial_settings:
    configuration = json.load(initial_settings)
    for entry in configuration["secure_computation_nodes"]:
        scn_names.append(entry["ip_address"])
        scn_ports.append(5556)
        list_dataset_id.append(entry["dataset_id"])


# TODO make this a other implementation that autoconfigures
# participant_service = ParticipantServiceClientDict()
# for dataset_id, scn_name, scn_port in zip(list_dataset_id, scn_names, scn_ports):
#     participant_service.register_client(dataset_id, ClientRPCZero(scn_name, scn_port))
#     print(f"Connected to SCN {scn_name} serving dataset {dataset_id}")


# implementation_manager = ImplementationManager.get_instance()
# implementation_manager.set_participant_service(participant_service)
# implementation_manager.initialize()

implementation_manager = ImplementationManager.get_instance()
implementation_manager.set_participant_service(ParticipantSeriviceLocal())
implementation_manager.initialize()


class DataFederation(BaseModel):
    list_dataset_id: List[str]


class Audit_log_task(threading.Thread):
    """
    Auxillary class for audit log server in isolated thread
    """

    def run(self):
        """
        Start async logger server
        """
        _AsyncLogger.start_log_poller(_AsyncLogger.ipc, _AsyncLogger.port)


@app.on_event("startup")
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


# DATA MODEL


@app.post(
    path="/new_data_frame_tabular/",
    description="Create new Tabular Data Model",
    response_description="Reference to generated tabular data model",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="new_tabular_model",
)
async def new_data_frame_tabular() -> dict:
    data_frame_tabular = DataModelTabular()
    data_frame_id = service_reference.get_instance().data_model_tabular_to_reference(data_frame_tabular)

    return {"data_frame_tabular_id": data_frame_id}


@app.post(
    path="/new_series_model_numerical",
    description="Create new numerical Series Model",
    response_description="Reference to generated numerical Series Model",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="new_series_model_numerical",
)
async def new_series_model_numerical(
    series_name: str = Body(description="name of the series"),
    measurement_source_name: str = Body(description="Source featuree of the series."),
    type_agregator: str = Body(description="Method by which source of data is to be aggregated"),
    unit: str = Body(description="The unit type of the series model"),
) -> dict:
    series = DataModelSeries.create_numerical(
        series_name=series_name,
        measurement_source_name=measurement_source_name,
        type_agregator=type_agregator,
        unit=unit,
    )
    series_id = service_reference.get_instance().data_model_series_to_reference(series)

    return {"series_id": series_id}


@app.post(
    path="/data_model_tabular_add_dataframe",
    description="Add a Dataframe model to a Tabular Dataframe Model",
    response_description="Reference to Tabular Dataframe Model",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="tabular_model_add_dataframe_model",
)
async def tabular_model_add_dataframe_model(
    data_model_tabular_id: str = Body(description="The reference to the Tabular Dataframe model being added to."),
    data_model_dataframe_id: str = Body(
        description="The reference to the Dataframe model being added to the Tabular Dataframe."
    ),
) -> dict:
    data_model_tabular = service_reference.get_instance().reference_to_data_model_tabular(data_model_tabular_id)
    data_model = service_reference.get_instance().reference_to_data_model_data_frame(data_model_dataframe_id)

    data_model_tabular.add_data_model_data_frame(data_model)

    return {"data_frame_tabular_id": data_model_tabular_id}


@app.post(
    path="/new_data_model_data_frame",
    description="Create a new Dataframe model.",
    response_description="Reference to Dataframe model",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="new_data_model_data_frame",
)
async def new_data_model_data_frame(
    data_frame_name: str = Body(description="Desired name of the new Dataframe"),
) -> dict:
    dataframe_id = ""
    if data_frame_name not in dataframe_name_lookup:
        new_dataframe = DataModelDataFrame(data_frame_name)
        dataframe_id = service_reference.get_instance().data_model_data_frame_to_reference(new_dataframe)
        dataframe_name_lookup[data_frame_name] = dataframe_id
    else:
        dataframe_id = dataframe_name_lookup[data_frame_name]

    return {"data_model_id": dataframe_id}


@app.post(
    path="/dataframe_model_add_new_series_model.",
    description="Create a new numerical series model and add it to a Dataframe model.",
    response_description="Reference to Dataframe model.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="dataframe_model_add_new_series_model",
)
async def dataframe_model_add_series_model(
    data_model_id: str = Body(description="Reference to the data model being added to."),
    series_name: str = Body(description="Name of the new series model to be added."),
    measurement_source_name: str = Body(description="The feature to aggregate."),
    type_agregator: str = Body(description="Method by which source of data is to be aggregated for new series model"),
    unit: str = Body(description="The unit of measurement of the new series to be added."),
) -> dict:
    data_model_data_frame = service_reference.get_instance().reference_to_data_model_data_frame(data_model_id)
    if data_model_data_frame is not None:
        data_model_data_frame.add_data_model_series(
            DataModelSeries.create_numerical(
                series_name=series_name,
                measurement_source_name=measurement_source_name,
                type_agregator=type_agregator,
                unit=unit,
            )
        )

    return {"data_model_id": data_model_id}


# DATA MODEL END
# DATA INGESTION
@app.post(
    path="/read_longitudinal_fhirv1.",
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


@app.post(
    path="/read_dataset_tabular_from_longitudinal.",
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
@app.post(
    path="/dataset_tabular_fhirv1.",
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


@app.post(
    path="/read_tabular_dataframe_csvv1.",
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


# DATA INGESTION END
# DATAFRAME MANIPULATION


@app.post(
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


@app.post(
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


# DATAFRAME_MANIPULATION END

# PREPROCESSING
# Doesn't work but we should allow it
# @app.post("/preprocessing/series/drop_missing/{series_id}")
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


@app.post(
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


@app.post(
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


# END PREPROCESSING

# STATS


@app.post(
    path="/statistics_chisquare.",
    description="Computes the chisquare of two Series.",
    response_description="The chisquare statistic and p value.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_chisquare",
)
async def statistics_chisquare(
    series_1_id: str = Body(description="The identifier of Series 1"),
    series_2_id: str = Body(description="The identifier of Series 2."),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    return {"chisquare": statistics.chisquare(series_1, series_2)}


@app.post(
    path="/statistics_count.",
    description="Computes the count of a Series.",
    response_description="The count of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_count",
)
@app.post("/statistics_count")
async def count(series_id: str = Body(description="The identifier of the series to be counted.")) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    await validate(series)
    return {"count": statistics.count(series)}


@app.post(
    path="/statistics_kolmogorov_smirnov_test",
    description="Computes Kolmogorov Smirnov Test of a Series.",
    response_description="The K statisic and P value of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_kolmogorov_smirnov_test",
)
async def kolmogorov_smirnov_test(
    series_1_id: str = Body(description="the identifier of the Series to be computed"),
    type_distribution: str = Body(description="Type of distribution of Series. May be 'normal' or 'normal unit'"),
) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_1_id)

    await validate(series)
    return {"kolmogorov_smirnov_test": statistics.kolmogorov_smirnov_test(series, type_distribution, "cdf")}


@app.post(
    path="/statistics_kurtosis",
    description="Computes Kurtosis of a Series.",
    response_description="The Kurtosis value of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_kurtosis",
)
async def kurtosis(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    await validate(series)
    return {"kurtosis": statistics.kurtosis(series)}


@app.post(
    path="/statistics_levene_test",
    description="Computes the Levene Test of two Series.",
    response_description="The F statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_levene_test",
)
async def levene_test(
    series_1_id: str = Body(description="The identifier of series 1."),
    series_2_id: str = Body(description="The identifier of series 2."),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    f_statistic_sail, p_value_sail = statistics.levene_test(series_1, series_2)

    return {"f_statistic": f_statistic_sail, "p_value": p_value_sail}


@app.post(
    path="/mann_whitney_u_test",
    description="Computes the Mann Whitney U Test of two Series.",
    response_description="The W statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="mann_whitney_u_test",
)
async def mann_whitney_u_test(
    series_1_id: str = Body(description="The identifer of Series 1."),
    series_2_id: str = Body(description="The identifier of Series 2."),
    alternative: str = Body(description="Alternative must be of 'less', 'two-sided' or 'greater'"),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    w_statistic_sail, p_value_sail = statistics.mann_whitney_u_test(series_1, series_2, alternative, "cdf")
    return {"w_statistic": w_statistic_sail, "p_value": p_value_sail}


@app.post(
    path="/statistics_mean",
    description="Computes the Mean of a Series.",
    response_description="The Series Mean.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_mean",
)
async def mean(series_id: str = Body(description="The identifer of the Series to be computed.")) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    await validate(series)

    return {"mean": statistics.mean(series)}


@app.post(
    path="/statistics_min_max",
    description="Computes the Min and Max of a Series.",
    response_description="The Series Min and Max.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_min_max",
)
async def min_max(series_id: str = Body(description="The identifer of the Series to be computed.")) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    await validate(series)

    min, max = statistics.min_max(series)
    return {"min": min, "max": max}


@app.post(
    path="/statistics_paired_t_test",
    description="Computes the Paired T Test of two Series.",
    response_description="The T statistic and P value of the two series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_paired_t_test",
)
async def paired_t_test(
    series_1_id: str = Body(description="Identifier of Series 1"),
    series_2_id: str = Body(description="Identifier of Series 2"),
    alternative: str = Body(description="Alternative must be of 'less', 'two-sided' or 'greater'"),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    t_statistic_sail, p_value_sail = statistics.paired_t_test(series_1, series_2, alternative)
    return {"t_statistic": t_statistic_sail, "p_value": p_value_sail}


@app.post(
    path="/statistics_pearson",
    description="Computes the Pearson of two Series.",
    response_description="The Pearson statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_pearson",
)
async def pearson(
    series_1_id: str = Body(description="Identifier of Series 1"),
    series_2_id: str = Body(description="Identifier of Series 2"),
    alternative: str = Body(description="Alternative must be of 'less', 'two-sided' or 'greater'"),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    pearson_sail, p_value_sail = statistics.pearson(series_1, series_2, alternative)
    return {"pearson": pearson_sail, "p_value": p_value_sail}


@app.post(
    path="/statistics_skewness",
    description="Computes the Skewness of a Series.",
    response_description="The Skewness of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_skewness",
)
async def skewness(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    await validate(series)

    return {"skewness": statistics.skewness(series)}


@app.post(
    path="/statistics_spearman",
    description="Computes the Spearman statistic of two Series.",
    response_description="The Spearman statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_spearman",
)
async def spearman(
    series_1_id: str = Body(description="Identifier of Series 1"),
    series_2_id: str = Body(description="Identifier of Series 2"),
    alternative: str = Body(description="Alternative must be of 'less', 'two-sided' or 'greater'"),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)
    spearman_sail, p_value_sail = statistics.spearman(series_1, series_2, alternative, "cdf")
    return {"spearman": spearman_sail, "p_value": p_value_sail}


@app.post(
    path="/statistics_student_t_test",
    description="Computes the Student T test of two Series.",
    response_description="The T statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_student_t_test",
)
async def student_t_test(
    series_1_id: str = Body(description="Identifier of Series 1"),
    series_2_id: str = Body(description="Identifier of Series 2"),
    alternative: str = Body(description="Alternative must be of 'less', 'two-sided' or 'greater'"),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    t_statistic_sail, p_value_sail = statistics.student_t_test(series_1, series_2, alternative)
    return {"t_statistic": t_statistic_sail, "p_value": p_value_sail}


@app.post(
    path="/statistics_variance",
    description="Computes the Variance of a Series.",
    response_description="The Variance of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_variance",
)
async def variance(series_id: str = Body(description="The identifier of the series")) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    await validate(series)

    return {"variance": statistics.variance(series)}


@app.post(
    path="/statistics_welch_t_test",
    description="Computes the Welch T test of two Series.",
    response_description="The T statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_welch_t_test",
)
async def welch_t_test(
    series_1_id: str = Body(description="Identifier of Series 1"),
    series_2_id: str = Body(description="Identifier of Series 2"),
    alternative: str = Body(description="Alternative must be of 'less', 'two-sided' or 'greater'"),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    t_statistic_sail, p_value_sail = statistics.welch_t_test(series_1, series_2, alternative)
    return {"t_statistic": t_statistic_sail, "p_value": p_value_sail}


@app.post(
    path="/statistics_wilcoxon_signed_rank_test",
    description="Computes the Wilcoxon signed rank test of two Series.",
    response_description="The W statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="statistics_wilcoxon_signed_rank_test",
)
async def wilcoxon_signed_rank_test(
    series_1_id: str = Body(description="Identifier of Series 1"),
    series_2_id: str = Body(description="Identifier of Series 2"),
    alternative: str = Body(description="Alternative must be of 'less', 'two-sided' or 'greater'"),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    w_statistic_sail, p_value_sail = statistics.spearman(series_1, series_2, alternative, "cdf")
    return {"w_statistic": w_statistic_sail, "p_value": p_value_sail}


# END STATS

# START VISUALIZATION
@app.post(
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


@app.post("/visualization_kernel_density_estimation")
@app.post(
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


# END VISUALIZATION
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

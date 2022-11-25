import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sail_safe_functions_orchestrator import preprocessing, statistics
from sail_safe_functions_orchestrator.client_rpc_zero import ClientRPCZero
from sail_safe_functions_orchestrator.data_model.data_model_data_frame import (
    DataModelDataFrame,
)
from sail_safe_functions_orchestrator.data_model.data_model_series import (
    DataModelSeries,
)
from sail_safe_functions_orchestrator.data_model.data_model_tabular import (
    DataModelTabular,
)
from sail_safe_functions_orchestrator.preprocessing import convert
from sail_safe_functions_orchestrator.service_client_dict import ServiceClientDict
from sail_safe_functions_test.helper_sail_safe_functions.test_service_reference import (
    TestServiceReference,
)

app = FastAPI()

service_reference = TestServiceReference.get_instance()

dataframe_name_lookup = {}

scn_names = ["127.0.0.1"]
list_dataset_id = []
list_dataset_id.append("a892ef90-4f6f-11ed-bdc3-0242ac120002")

service_client = ServiceClientDict()
for dataset_id, scn_name in zip(list_dataset_id, scn_names):
    service_client.register_client(dataset_id, ClientRPCZero(scn_name, 5010))
    print(f"Connected to SCN serving dataset {scn_name}")


@app.get("/")
async def root():
    """
    Redirects user to docs as hompage
    """
    return RedirectResponse("/docs")


def get_series(series_uuid: str):
    return service_reference.reference_to_federated_series(series_uuid)


def get_dataframe(dataframe_uuid: str):
    return service_reference.reference_to_federated_dataframe(dataframe_uuid)


def query_limit_n(series, n=10) -> bool:
    """
    Checks data or series in question is over a given threshold.

    :param: data: the data item being checked
    :type: remote dataframe or remote series
    :return: True or False relating to whether the threshold has been surpassed
    :type: Boolean
    """
    return statistics.count(series) > n


def validate(series) -> bool:
    """
    Validates execution criteria for data inputs
    :param: data: the data item being validated
    :type: Remote Dataframe or Remote Series
    :return: sample series
    :type: Error message or True condition depending on whether validation passes
    """

    # Check query limit N
    if not query_limit_n(series):
        return {"payload": "Error: Federation Length Too Small"}
    else:
        return True

    # CHECKS
    # TODO:
    #       1. Check for pandas query injection in column_id string
    # CLOSE CHECKS


@app.post("/admin/get_dataframe_name_lookup_table")
async def get_dataframe_name_lookup_table() -> dict:
    return {"dataframe_name_lookup": dataframe_name_lookup}


## DATA MODEL


@app.post("/data_model/new_tabular_model")
async def data_frame_tabular() -> dict:
    data_frame_tabular = DataModelTabular()
    data_frame_id = service_reference.get_instance().data_model_tabular_to_reference(
        data_frame_tabular
    )

    return {"data_frame_tabular_id": data_frame_id}


@app.post("/data_model/tabular/{data_model_tabular_id}/add_dataframe")
async def tabular_model_add_dataframe_model(
    data_model_tabular_id: str, data_model_dataframe_id: str
) -> dict:
    data_model_tabular = (
        service_reference.get_instance().reference_to_data_model_tabular(
            data_model_tabular_id
        )
    )
    data_model = service_reference.get_instance().reference_to_data_model_data_frame(
        data_model_dataframe_id
    )

    data_model_tabular.add_data_model_data_frame(data_model)

    return {"data_frame_tabular_id": data_model_tabular_id}


@app.post("/data_model/new_data_frame_model")
async def create_data_model_data_frame(data_frame_name: str) -> dict:
    dataframe_id = ""
    if data_frame_name not in dataframe_name_lookup:
        new_dataframe = DataModelDataFrame(data_frame_name)
        dataframe_id = (
            service_reference.get_instance().data_model_data_frame_to_reference(
                new_dataframe
            )
        )
        dataframe_name_lookup[data_frame_name] = dataframe_id
    else:
        dataframe_id = dataframe_name_lookup[data_frame_name]

    return {"data_model_id": dataframe_id}


@app.post("/data_model/data_frame/{data_model_id}/add_new_series_model")
async def data_model_add_series_model(
    data_model_id: str, series_name: str, measurement_source_name: str
) -> dict:
    data_model_data_frame = (
        service_reference.get_instance().reference_to_data_model_data_frame(
            data_model_id
        )
    )
    if data_model_data_frame is not None:
        data_model_data_frame.add_data_model_series(
            DataModelSeries.create_numerical(
                series_name=series_name,
                measurement_source_name=measurement_source_name,
                type_agregator=DataModelSeries.AgregatorIntervalMean,
                unit="kg/m2",
            )
        )

    return {"data_model_id": data_model_id}


## DATA MODEL END
## DATA INGESTION
@app.post("/ingestion/dataset_tabular/fhirv1")
async def dataset_tabular_fhirv1(
    dataset_federation_id: str, dataset_federation_name: str, data_model_tabular_id: str
) -> dict:
    dataset_longitudinal = preprocessing.read_dataset_fhirv1(
        service_client, list_dataset_id
    )
    data_model_tablular = (
        service_reference.get_instance().reference_to_data_model_tabular(
            data_model_tabular_id
        )
    )

    dataset_tabular = convert.convert_to_dataset_tabular(
        dataset_longitudinal,
        dataset_federation_id,
        dataset_federation_name,
        data_model_tablular,
    )

    dataset_id = service_reference.get_instance().data_set_tabular_to_reference(
        dataset_tabular
    )

    return {"dataset_id": dataset_id}


## DATA INGESTION END
## STATS


@app.post("/statistics/chisquare/{series_1_id}/{series_2_id}")
async def chisquare(series_1_id: str, series_2_id: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(
        series_1_id
    )
    series_2 = service_reference.get_instance().reference_to_federated_series(
        series_2_id
    )
    validate(series_1)
    validate(series_2)

    return {"chisquare": statistics.chisquare(series_1, series_2)}


@app.post("/statistics/count/{series_id}")
async def count(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    validate(series)
    return {"count": statistics.count(series)}


@app.post("/statistics/kolmogorovSmirnovTest/{series_1_id}")
async def chisquare(
    series_1_id: str, type_distribution: str, type_ranking: str
) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_1_id)

    validate(series)

    return {
        "kolmogorov_smirnov_test": statistics.kolmogorov_smirnov_test(
            series, type_distribution, type_ranking
        )
    }


@app.post("/statistics/kurtosis/{series_id}")
async def kurtosis(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    validate(series)

    return {"kurtosis": statistics.kurtosis(series)}


@app.post("/statistics/levene_test/{series_1_id}/{series_2_id}")
async def levene_test(series_1_id: str, series_2_id: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(
        series_1_id
    )
    series_2 = service_reference.get_instance().reference_to_federated_series(
        series_2_id
    )
    validate(series_1)
    validate(series_2)
    f_statistic_sail, p_value_sail = statistics.levene_test(series_1, series_2)
    return {"f_statistic_sail": f_statistic_sail, "p_value_sail": p_value_sail}


@app.post("/statistics/mann_whitney_u_test/{series_1_id}/{series_2_id}")
async def mann_whitney_u_test(
    series_1_id: str, series_2_id: str, alternative: str, type_ranking: str
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(
        series_1_id
    )
    series_2 = service_reference.get_instance().reference_to_federated_series(
        series_2_id
    )

    validate(series_1)
    validate(series_2)

    w_statistic_sail, p_value_sail = statistics.mann_whitney_u_test(
        series_1, series_2, alternative, type_ranking
    )

    return {"w_statistic_sail": w_statistic_sail, "p_value_sail": p_value_sail}


@app.post("/statistics/mean/{series_id}")
async def mean(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    validate(series)

    return {"mean": statistics.mean(series)}


@app.post("/statistics/min_max/{series_id}")
async def min_max(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    validate(series)

    min, max = statistics.min_max(series)

    return {"min_sail": min, "max_sail": max}


@app.post("/statistics/paired_t_test/{series_1_id}/{series_2_id}")
async def paired_t_test(series_1_id: str, series_2_id: str, alternative: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(
        series_1_id
    )
    series_2 = service_reference.get_instance().reference_to_federated_series(
        series_2_id
    )

    validate(series_1)
    validate(series_2)

    t_statistic_sail, p_value_sail = statistics.paired_t_test(
        series_1, series_2, alternative
    )

    return {"t_statistic_sail": t_statistic_sail, "p_value_sail": p_value_sail}


@app.post("/statistics/pearson/{series_1_id}/{series_2_id}")
async def pearson(series_1_id: str, series_2_id: str, alternative: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(
        series_1_id
    )
    series_2 = service_reference.get_instance().reference_to_federated_series(
        series_2_id
    )

    validate(series_1)
    validate(series_2)

    pearson_sail, p_value_sail = statistics.pearson(series_1, series_2, alternative)

    return {"pearson_sail": pearson_sail, "p_value_sail": p_value_sail}


@app.post("/statistics/skewness/{series_id}")
async def skewness(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    validate(series)
    return {"skewness_sail": statistics.skewness(series)}


@app.post("/statistics/spearman/{series_1_id}/{series_2_id}")
async def spearman(
    series_1_id: str, series_2_id: str, alternative: str, type_ranking: str
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(
        series_1_id
    )
    series_2 = service_reference.get_instance().reference_to_federated_series(
        series_2_id
    )

    validate(series_1)
    validate(series_2)

    spearman_sail, p_value_sail = statistics.spearman(
        series_1, series_2, alternative, type_ranking
    )

    return {"spearman_sail": spearman_sail, "p_value_sail": p_value_sail}


@app.post("/statistics/student_t_test/{series_1_id}/{series_2_id}")
async def student_t_test(series_1_id: str, series_2_id: str, alternative: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(
        series_1_id
    )
    series_2 = service_reference.get_instance().reference_to_federated_series(
        series_2_id
    )

    validate(series_1)
    validate(series_2)

    t_statistic_sail, p_value_sail = statistics.student_t_test(
        series_1, series_2, alternative
    )

    return {"t_statistic_sail": t_statistic_sail, "p_value_sail": p_value_sail}


@app.post("/statistics/variance/{series_id}")
async def variance(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    validate(series)
    return {"variance_sail": statistics.variance(series)}


@app.post("/statistics/welch_t_test/{series_1_id}/{series_2_id}")
async def welch_t_test(series_1_id: str, series_2_id: str, alternative: str) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(
        series_1_id
    )
    series_2 = service_reference.get_instance().reference_to_federated_series(
        series_2_id
    )

    validate(series_1)
    validate(series_2)

    t_statistic_sail, p_value_sail = statistics.welch_t_test(
        series_1, series_2, alternative
    )

    return {"t_statistic_sail": t_statistic_sail, "p_value_sail": p_value_sail}


@app.post("/statistics/wilcoxon_signed_rank_test/{series_1_id}/{series_2_id}")
async def spearman(
    series_1_id: str, series_2_id: str, alternative: str, type_ranking: str
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(
        series_1_id
    )
    series_2 = service_reference.get_instance().reference_to_federated_series(
        series_2_id
    )

    validate(series_1)
    validate(series_2)

    w_statistic_sail, p_value_sail = statistics.spearman(
        series_1, series_2, alternative, type_ranking
    )

    return {"w_statistic_sail": w_statistic_sail, "p_value_sail": p_value_sail}


## END STATS
## DATAFRAME MANIPULATION


@app.post("/data_frame_tabular/select_dataframe/{data_frame_tabular_id}")
async def data_frame_tabular_select_dataframe(
    data_frame_tabular_id: str, data_frame_name: str
) -> dict:
    data_frame_tabular = service_reference.get_instance().reference_to_data_set_tabular(
        data_frame_tabular_id
    )
    data_frame = data_frame_tabular[data_frame_name]

    data_frame_id = service_reference.get_instance().federated_dataframe_to_reference(
        data_frame
    )
    return {"data_frame_id": data_frame_id}


@app.post("/data_frame/select_series/{data_frame_id}")
async def data_frame_select_series(data_frame_id: str, series_name: str) -> dict:
    data_frame = service_reference.get_instance().reference_to_federated_dataframe(
        data_frame_id
    )
    series = data_frame[series_name]

    series_id = service_reference.get_instance().federated_series_to_reference(series)
    return {"series_id": series_id}


## DATAFRAME_MANIPULATION
## PREPROCESSING


@app.post("/preprocessing/data_frame/drop_missing/{dataset_id}/{data_frame_name}")
async def drop_missing(dataset_id: str, data_frame_name: str) -> dict:
    dataset_tabular = service_reference.get_instance().reference_to_data_set_tabular(
        dataset_id
    )

    orig_data_frame = dataset_tabular[data_frame_name]

    new_data_frame = preprocessing.drop_missing(
        orig_data_frame, axis=0, how="any", thresh=None, subset=None
    )

    new_data_frame_id = (
        service_reference.get_instance().federated_dataframe_to_reference(
            new_data_frame
        )
    )

    return {"result_data_frame_id": new_data_frame_id}


if __name__ == "__main__":

    # Specific aguments
    # 20_1
    # a892ef90-4f6f-11ed-bdc3-0242ac120002

    # 60_1
    # a892ffd0-4f6f-11ed-bdc3-0242ac120002
    # a89301b0-4f6f-11ed-bdc3-0242ac120002
    # a89302dc-4f6f-11ed-bdc3-0242ac120002

    # Arrange
    dataset_federation_id = "a892f738-4f6f-11ed-bdc3-0242ac120002"
    dataset_federation_name = "r4sep2019_csvv1_20_1"
    data_frame_name = "data_frame_0"

    data_model_data_frame = DataModelDataFrame(data_frame_name)
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_mean",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalMean,
            unit="kg/m2",
        )
    )
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_first",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalFirstOccurance,
            unit="kg/m2",
        )
    )

    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_last",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalLastOccurance,
            unit="kg/m2",
        )
    )
    data_model_tablular = DataModelTabular()
    data_model_tablular.add_data_model_data_frame(data_model_data_frame)

    # act
    dataset_longitudinal = preprocessing.read_dataset_fhirv1(
        service_client, list_dataset_id
    )
    dataset_tabular = convert.convert_to_dataset_tabular(
        dataset_longitudinal,
        dataset_federation_id,
        dataset_federation_name,
        data_model_tablular,
    )
    data_frame_nan = dataset_tabular[data_frame_name]
    name_series_1 = data_frame_nan.list_series_name[1]
    print(
        f"Number of entires including NaN: {statistics.count(data_frame_nan[name_series_1])}"
    )

    data_frame_nonan = preprocessing.drop_missing(
        data_frame_nan, axis=0, how="any", thresh=None, subset=None
    )
    print(
        f"Number of entires excluding NaN: {statistics.count(data_frame_nonan[name_series_1])}"
    )
    series_1 = data_frame_nonan[name_series_1]
    mean_1 = statistics.mean(series_1)

    print(f"Mean of {name_series_1}: {mean_1}")

    print(f"Data frame {data_frame_nonan}")
    print(f"Series {series_1}")
    print(f"Series datasets {series_1.list_dataset_id}")
    print(f"Tabular dataset {dataset_tabular}")
    print(f"Model dataset {data_model_tablular.list_data_frame_name}")

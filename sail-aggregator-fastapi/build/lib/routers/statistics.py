
from fastapi import Body, Depends, FastAPI, HTTPException, Path, Response, status
from fastapi import APIRouter
from sail_safe_functions.test.helper_sail_safe_functions.test_service_reference import TestServiceReference
from sail_safe_functions.aggregator import statistics
from sail_safe_functions.aggregator.statistics import wilcoxon_singed_rank_test
import config
from config import validate, query_limit_n

import os
import json
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
    prefix='/statistics',
)

@router.post(
    path="/chisquare",
    description="Computes the chisquare of two Series.",
    response_description="The chisquare statistic and p value.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="chisquare",
)
async def chisquare(
    series_1_id: str = Body(description="The identifier of Series 1"),
    series_2_id: str = Body(description="The identifier of Series 2."),
) -> dict:
    series_1 = service_reference.get_instance().reference_to_federated_series(series_1_id)
    series_2 = service_reference.get_instance().reference_to_federated_series(series_2_id)

    await validate(series_1)
    await validate(series_2)

    return {"chisquare": statistics.chisquare(series_1, series_2)}


@router.post(
    path="/count.",
    description="Computes the count of a Series.",
    response_description="The count of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="count",
)
async def count(series_id: str = Body(description="The identifier of the series to be counted.")) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    await validate(series)
    return {"count": statistics.count(series)}


@router.post(
    path="/kolmogorov_smirnov_test",
    description="Computes Kolmogorov Smirnov Test of a Series.",
    response_description="The K statisic and P value of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="kolmogorov_smirnov_test",
)
async def kolmogorov_smirnov_test(
    series_1_id: str = Body(description="the identifier of the Series to be computed"),
    type_distribution: str = Body(description="Type of distribution of Series. May be 'normal' or 'normal unit'"),
) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_1_id)

    await validate(series)
    return {"kolmogorov_smirnov_test": statistics.kolmogorov_smirnov_test(series, type_distribution, "cdf")}


@router.post(
    path="/kurtosis",
    description="Computes Kurtosis of a Series.",
    response_description="The Kurtosis value of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="kurtosis",
)
async def kurtosis(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    await validate(series)
    return {"kurtosis": statistics.kurtosis(series)}


@router.post(
    path="/levene_test",
    description="Computes the Levene Test of two Series.",
    response_description="The F statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="levene_test",
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

@router.post(
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


@router.post(
    path="/mean",
    description="Computes the Mean of a Series.",
    response_description="The Series Mean.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="mean",
)
async def mean(series_id: str = Body(description="The identifer of the Series to be computed.")) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    await validate(series)

    return {"mean": statistics.mean(series)}


@router.post(
    path="/min_max",
    description="Computes the Min and Max of a Series.",
    response_description="The Series Min and Max.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="min_max",
)
async def min_max(series_id: str = Body(description="The identifer of the Series to be computed.")) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)

    await validate(series)

    min, max = statistics.min_max(series)
    return {"min": min, "max": max}

@router.post(
    path="/paired_t_test",
    description="Computes the Paired T Test of two Series.",
    response_description="The T statistic and P value of the two series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="paired_t_test",
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


@router.post(
    path="/pearson",
    description="Computes the Pearson of two Series.",
    response_description="The Pearson statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="pearson",
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


@router.post(
    path="/skewness",
    description="Computes the Skewness of a Series.",
    response_description="The Skewness of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="skewness",
)
async def skewness(series_id: str) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    await validate(series)

    return {"skewness": statistics.skewness(series)}


@router.post(
    path="/spearman",
    description="Computes the Spearman statistic of two Series.",
    response_description="The Spearman statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="spearman",
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


@router.post(
    path="/student_t_test",
    description="Computes the Student T test of two Series.",
    response_description="The T statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="student_t_test",
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


@router.post(
    path="/variance",
    description="Computes the Variance of a Series.",
    response_description="The Variance of the Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="variance",
)
async def variance(series_id: str = Body(description="The identifier of the series")) -> dict:
    series = service_reference.get_instance().reference_to_federated_series(series_id)
    await validate(series)

    return {"variance": statistics.variance(series)}


@router.post(
    path="/welch_t_test",
    description="Computes the Welch T test of two Series.",
    response_description="The T statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="welch_t_test",
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


@router.post(
    path="/wilcoxon_signed_rank_test",
    description="Computes the Wilcoxon signed rank test of two Series.",
    response_description="The W statistic and P value of the two Series.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="wilcoxon_signed_rank_test",
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

    w_statistic_sail, p_value_sail = wilcoxon_singed_rank_test(series_1, series_2, alternative, "cdf")
    return {"w_statistic": w_statistic_sail, "p_value": p_value_sail}

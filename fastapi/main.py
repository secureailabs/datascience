from fastapi import FastAPI
from sail_safe_functions_orchestrator.statistics.kolmogorov_smirnov_test import (
    KolmogorovSmirnovTest,
)
from sail_safe_functions_orchestrator.statistics.kurtosis import Kurtosis
from sail_safe_functions_orchestrator.statistics.mean import Mean
from sail_safe_functions_orchestrator.statistics.chisquare import Chisquare

from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import (
    DataFrameFederatedLocal,
)

from fastapi.responses import RedirectResponse
from SecureUtility import validate, get_series


app = FastAPI()


@app.get("/")
async def root():
    return RedirectResponse("/docs")


@app.get("/mean")
async def mean(series_uuid: str):
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = Mean()
    payload = estimator.run(series)

    # Return
    return {"payload": payload}


@app.get("/chisquare")
async def chisquare(series_uuid_1: str, series_uuid_2: str):
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = Chisquare()
    payload = estimator.run(series_1, series_2)

    # Return
    return {"payload": payload}


@app.get("/kolmogorovSmirnovTest")
async def chisquare(series_uuid: str, type_distribution: str, type_ranking: str):
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = KolmogorovSmirnovTest(
        type_distribution=type_distribution, type_ranking=type_ranking
    )
    k_statistic_sail, p_value_sail = estimator.run(series)

    # Return
    return {"k_statistic_sail": k_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/kurtosis")
async def kurtosis(series_uuid: str):
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = Kurtosis()
    kurtosis_sail = estimator.run(series)

    # Return
    return {"kurtosis_sail": kurtosis_sail}

from fastapi import FastAPI
from sail_safe_functions_orchestrator.statistics.kolmogorov_smirnov_test import (
    KolmogorovSmirnovTest,
)
from sail_safe_functions_orchestrator.statistics.kurtosis import Kurtosis
from sail_safe_functions_orchestrator.statistics.levene_test import LeveneTest
from sail_safe_functions_orchestrator.statistics.mann_whitney_u_test import (
    MannWhitneyUTest,
)
from sail_safe_functions_orchestrator.statistics.mean import Mean
from sail_safe_functions_orchestrator.statistics.chisquare import Chisquare
from sail_safe_functions_orchestrator.statistics.min_max import MinMax
from sail_safe_functions_orchestrator.statistics.paired_t_test import PairedTTest
from sail_safe_functions_orchestrator.statistics.pearson import Pearson
from sail_safe_functions_orchestrator.statistics.skewness import Skewness
from sail_safe_functions_orchestrator.statistics.spearman import Spearman
from sail_safe_functions_orchestrator.statistics.student_t_test import StudentTTest
from sail_safe_functions_orchestrator.statistics.variance import Variance
from sail_safe_functions_orchestrator.statistics.wilcoxon_signed_rank_test import (
    WilcoxonSingedRankTest,
)


from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import (
    DataFrameFederatedLocal,
)

from fastapi.responses import RedirectResponse
from SecureUtility import validate, get_series, get_series_different


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
    return {"mean_sail": payload}


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
    return {"chisquare_sail": payload}


@app.get("/kolmogorovSmirnovTest")
async def kolmogorovSmirnovTest(
    series_uuid: str, type_distribution: str, type_ranking: str
):
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


@app.get("/leveneTest")
async def leveneTest(series_uuid_1: str, series_uuid_2: str):
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = LeveneTest()
    f_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"f_statistic_sail": f_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/mannWhitneyUTest")
async def mannWhitneyUTest(
    series_uuid_1: str, series_uuid_2: str, alternative: str, type_ranking: str
):
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = MannWhitneyUTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"w_statistic_sail": w_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/minMax")
async def minMax(series_uuid: str):
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = MinMax()
    min_sail, max_sail = estimator.run(series)

    # Return
    return {"min_sail": min_sail, "max_sail": max_sail}


@app.get("/pairedTTest")
async def pairedTTest(series_uuid_1: str, series_uuid_2: str, alternative: str):
    # Arrange
    series_1 = get_series()
    series_2 = get_series_different()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = PairedTTest(alternative=alternative)
    t_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"t_statistic_sail": t_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/pearson")
async def pearson(series_uuid_1: str, series_uuid_2: str, alternative: str):
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = Pearson(alternative=alternative)
    pearson_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"pearson_sail": pearson_sail, "p_value_sail": p_value_sail}


@app.get("/skewness")
async def skewness(series_uuid: str):
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = Skewness()
    skewness_sail = estimator.run(series)

    # Return
    return {"skewness_sail": skewness_sail}


@app.get("/spearman")
async def spearman(
    series_uuid_1: str, series_uuid_2: str, alternative: str, type_ranking: str
):
    # Arrange
    series_1 = get_series()
    series_2 = get_series_different()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    spearman_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"spearman_sail": spearman_sail, "p_value_sail": p_value_sail}


@app.get("/studentTTest")
async def studentTTest(series_uuid_1: str, series_uuid_2: str, alternative: str):
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = StudentTTest(alternative=alternative)
    t_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"t_statistic_sail": t_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/variance")
async def variance(series_uuid: str):
    # Arrange
    series = get_series()

    # Validate
    validate(series)

    # Execute
    estimator = Variance()
    variance_sail = estimator.run(series)

    # Return
    return {"variance_sail": variance_sail}


@app.get("/welchTTest")
async def welchTTest(series_uuid_1: str, series_uuid_2: str, alternative: str):
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = StudentTTest(alternative=alternative)
    t_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"t_statistic_sail": t_statistic_sail, "p_value_sail": p_value_sail}


@app.get("/wilcoxonSignedRankTest")
async def wilcoxonSignedRankTest(
    series_uuid_1: str, series_uuid_2: str, alternative: str, type_ranking: str
):
    # Arrange
    series_1 = get_series()
    series_2 = get_series()

    # Validate
    validate(series_1)
    validate(series_2)

    # Execute
    estimator = WilcoxonSingedRankTest(
        alternative=alternative, type_ranking=type_ranking
    )
    w_statistic_sail, p_value_sail = estimator.run(series_1, series_2)

    # Return
    return {"w_statistic_sail": w_statistic_sail, "p_value_sail": p_value_sail}

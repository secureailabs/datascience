import numpy
import pytest
from sail_safe_functions_orchestrator.statistics.kolmogorov_smirnov_test import (
    KolmogorovSmirnovTest,
)
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)
from scipy import stats
from sklearn.utils import estimator_html_repr


@pytest.mark.active
def test_kolmogorov_smirnov_normalunit():
    """
    Preform a kolmogorov_smirnov test for normality
    """
    # Arrange
    numpy.random.seed(42)
    array_sample_0 = numpy.random.normal(0, 1, 17)  # works from size 17 onwards
    sample_0 = SeriesFederatedLocal.from_array("dataset_0", "series_0", array_sample_0)
    # Act
    estimator = KolmogorovSmirnovTest(
        type_distribution="normalunit", type_ranking="unsafe"
    )
    k_statistic_sail, p_value_sail = estimator.run(sample_0)
    k_statistic_scipy, p_value_scipy = estimator.run_reference(sample_0)

    # Assert
    assert k_statistic_sail == pytest.approx(k_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)

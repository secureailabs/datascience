from typing import Tuple

import numpy
import pytest
from sail_safe_functions.aggregator.statistics.kolmogorov_smirnov_test import KolmogorovSmirnovTest
from sail_safe_functions.test.helper_sail_safe_functions.estimator_one_sample_reference import (
    EstimatorOneSampleReference,
)
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import ToolsDataTest
from sklearn.utils import estimator_html_repr


@pytest.mark.active
def test_kolmogorov_smirnov_normalunit():
    """Preform a kolmogorov_smirnov test for normality"""
    # Arrange
    numpy.random.seed(42)
    array_sample_0 = numpy.random.normal(0, 1, 17)  # works from size 17 onwards
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", array_sample_0)
    # Act
    estimator = KolmogorovSmirnovTest(type_distribution="normalunit", type_ranking="unsafe")
    k_statistic_sail, p_value_sail = estimator.run(sample_0)
    estimator_reference = EstimatorOneSampleReference(estimator)
    k_statistic_scipy, p_value_scipy = estimator_reference.run(sample_0)

    # Assert
    assert k_statistic_sail == pytest.approx(k_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)


@pytest.mark.active
def test_ks_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = KolmogorovSmirnovTest(type_distribution="normalunit", type_ranking="unsafe")

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_ks_one_value():
    """
    This is our test to raise exception for series containing only one value
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    # Act
    estimator = KolmogorovSmirnovTest(type_distribution="normalunit", type_ranking="unsafe")

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)


@pytest.mark.active
def test_ks_nan_value():
    """
    This is our test to raise exception if series containing nan values
    """
    # Arrange
    numpy.random.seed(42)
    a = numpy.empty((20))
    a[12:] = numpy.nan

    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", a)
    # Act
    estimator = KolmogorovSmirnovTest(type_distribution="normalunit", type_ranking="unsafe")

    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0)

    # Assert
    assert "series cannot containt nan or None values" in str(exc_info.value)

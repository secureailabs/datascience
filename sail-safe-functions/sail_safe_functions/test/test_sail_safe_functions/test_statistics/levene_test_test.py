from typing import Tuple

import numpy
import pytest
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.levene_test import LeveneTest
from sail_safe_functions.test.helper_sail_safe_functions.estimator_two_sample_reference import (
    EstimatorTwoSampleReference,
)
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import ToolsDataTest


@pytest.mark.active
def test_levene(two_sample_small_two: Tuple[SeriesFederated, SeriesFederated]):
    """
    This is our test for the Sails federated Levene test

    :param two_sample_small_two:
    :type two_sample_small_two: Tuple[SeriesFederated, SeriesFederated]
    """
    # Arrange
    sample_0 = two_sample_small_two[0]
    sample_1 = two_sample_small_two[1]

    # Act
    estimator = LeveneTest()
    f_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    estimator_reference = EstimatorTwoSampleReference(estimator)
    f_statistic_scipy, p_value_scipy = estimator_reference.run(sample_0, sample_1)

    # Assert
    assert f_statistic_scipy == pytest.approx(f_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_levens_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    estimator = LeveneTest()

    # Act
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_levens_one_value():
    """
    This is our test to raise exception for series containing only one value

    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    estimator = LeveneTest()

    # Act
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)


@pytest.mark.active
def test_levens_nan_value():
    """
    This is our test to raise exception if series containing nan values

    """
    # Arrange
    numpy.random.seed(42)
    a = numpy.empty((20))
    a[12:] = numpy.nan
    sample_size = 20
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", a)
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    estimator = LeveneTest()

    # Act
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt nan or None values" in str(exc_info.value)

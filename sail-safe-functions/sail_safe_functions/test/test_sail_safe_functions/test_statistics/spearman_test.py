from typing import Tuple

import numpy
import pytest
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.spearman import Spearman
from sail_safe_functions.test.helper_sail_safe_functions.estimator_two_sample_reference import (
    EstimatorTwoSampleReference,
)
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import ToolsDataTest


@pytest.mark.active
def test_spearman_two_sided(two_sample_big: Tuple[SeriesFederated, SeriesFederated]):
    """
    This is our test for the Sails federated Spearman

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederated, SeriesFederated]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]
    sample_size = 10
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "two-sided"
    type_ranking = "unsafe"

    # Act
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    spearman_sail, p_value_sail = estimator.run(sample_0, sample_1)
    estimator_reference = EstimatorTwoSampleReference(estimator)
    spearman_scipy, p_value_scipy = estimator_reference.run(sample_0, sample_1)

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_spearman_two_sided_2(two_sample_big: Tuple[SeriesFederated, SeriesFederated]):
    """
    This is our test for the Sails federated Spearman with different mean and standard deviation

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederated, SeriesFederated]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]
    sample_size = 10
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(2, 5, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "two-sided"
    type_ranking = "unsafe"

    # Act
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    spearman_sail, p_value_sail = estimator.run(sample_0, sample_1)
    estimator_reference = EstimatorTwoSampleReference(estimator)
    spearman_scipy, p_value_scipy = estimator_reference.run(sample_0, sample_1)

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_spearman_less(two_sample_big: Tuple[SeriesFederated, SeriesFederated]):
    """
    This is our test for the Sails federated Spearman

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederated, SeriesFederated]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]
    alternative = "less"
    type_ranking = "unsafe"

    # Act
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    spearman_sail, p_value_sail = estimator.run(sample_0, sample_1)
    estimator_reference = EstimatorTwoSampleReference(estimator)
    spearman_scipy, p_value_scipy = estimator_reference.run(sample_0, sample_1)

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_spearman_less_2(two_sample_big: Tuple[SeriesFederated, SeriesFederated]):
    """
    This is our test for the Sails federated Spearman with different mean and standard deviation.

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederated, SeriesFederated]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]
    sample_size = 10
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(2, 5, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "less"
    type_ranking = "unsafe"

    # Act
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    spearman_sail, p_value_sail = estimator.run(sample_0, sample_1)
    estimator_reference = EstimatorTwoSampleReference(estimator)
    spearman_scipy, p_value_scipy = estimator_reference.run(sample_0, sample_1)

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_spearman_greater(two_sample_big: Tuple[SeriesFederated, SeriesFederated]):
    """
    This is our test for the Sails federated Spearman with different mean and standard deviation

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederated, SeriesFederated]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]
    alternative = "greater"
    type_ranking = "unsafe"

    # Act
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    spearman_sail, p_value_sail = estimator.run(sample_0, sample_1)
    estimator_reference = EstimatorTwoSampleReference(estimator)
    spearman_scipy, p_value_scipy = estimator_reference.run(sample_0, sample_1)

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_spearman_greater_2(two_sample_big: Tuple[SeriesFederated, SeriesFederated]):
    """
    This is our test for the Sails federated Spearman with different mean and standard deviation

    :param two_sample_big:
    :type two_sample_big: Tuple[SeriesFederated, SeriesFederated]
    """
    # Arrange
    sample_0 = two_sample_big[0]
    sample_1 = two_sample_big[1]
    sample_size = 10
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(2, 5, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "greater"
    type_ranking = "unsafe"

    # Act
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    spearman_sail, p_value_sail = estimator.run(sample_0, sample_1)
    estimator_reference = EstimatorTwoSampleReference(estimator)
    spearman_scipy, p_value_scipy = estimator_reference.run(sample_0, sample_1)

    # Assert
    assert spearman_scipy == pytest.approx(spearman_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_spearman_empty():
    """
    This is our test to raise exception for empty
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "greater"
    type_ranking = "unsafe"

    # Act
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_spearman_one_value():
    """
    This is our test to raise exception for series containing only one value
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 1
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "greater"
    type_ranking = "unsafe"

    # Act
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

        # Assert
        assert "series cannot containt only one value" in str(exc_info.value)


@pytest.mark.active
def test_spearman_nan_value():
    """
    This is our test to raise exception for series containing nan value
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 20
    a = numpy.empty((20))
    a[12:] = numpy.nan
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", a)
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "greater"
    type_ranking = "unsafe"

    # Act
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt nan or None values" in str(exc_info.value)


@pytest.mark.active
def test_spearman_constant_value():
    """
    This is our test to raise exception for series containing constant value.
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 8
    a = [1, 1, 1, 1, 1, 1, 1, 1]
    a = numpy.array(a)
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", a)
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "greater"
    type_ranking = "unsafe"

    # Act
    estimator = Spearman(alternative=alternative, type_ranking=type_ranking)
    with pytest.raises(Exception) as exc_info:
        estimator.run(sample_0, sample_1)

    # Assert
    assert "Variance is zero raises sys.float_info.max" in str(exc_info.value)

import numpy
import pytest
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.aggregator.statistics.wilcoxon_signed_rank_test import WilcoxonSingedRankTest
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import ToolsDataTest


@pytest.mark.active
def test_wilcoxon_singed_rank_test_two_sided():
    """
    This is our test for the two-sided wilcoxon singed rank test
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 200
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "two-sided"
    type_ranking = "unsafe"

    # Act
    estimator = WilcoxonSingedRankTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    w_statistic_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_wilcoxon_singed_rank_test_two_sided_2():
    """
    This is our test for the two-sided wilcoxon singed rank test with different mean and standard deviation.
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 200
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(2, 5, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))

    alternative = "two-sided"
    type_ranking = "unsafe"

    # Act
    estimator = WilcoxonSingedRankTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    w_statistic_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_wilcoxon_singed_rank_test_less():
    """
    This is our test for the less wilcoxon singed rank test
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 200
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))

    alternative = "less"
    type_ranking = "unsafe"

    # Act
    estimator = WilcoxonSingedRankTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    w_statistic_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_wilcoxon_singed_rank_test_less_2():
    """
    This is our test for the less wilcoxon singed rank test with different mean and standard deviation
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 200
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(2, 5, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))

    alternative = "less"
    type_ranking = "unsafe"

    # Act
    estimator = WilcoxonSingedRankTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    w_statistic_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_wilcoxon_singed_rank_test_greater():
    """
    This is our test for the less wilcoxon singed rank test
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 200
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "greater"
    type_ranking = "unsafe"

    # Act
    estimator = WilcoxonSingedRankTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    w_statistic_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_wilcoxon_singed_rank_test_greater_2():
    """
    This is our test for the less wilcoxon singed rank test with different mean and standard deviation
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 200
    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(2, 5, sample_size))
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "greater"
    type_ranking = "unsafe"

    # Act
    estimator = WilcoxonSingedRankTest(alternative=alternative, type_ranking=type_ranking)
    w_statistic_sail, p_value_sail = estimator.run(sample_0, sample_1)
    w_statistic_scipy, p_value_scipy = estimator.run_reference(sample_0, sample_1)

    # Assert
    assert w_statistic_scipy == pytest.approx(w_statistic_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)


@pytest.mark.active
def test_wilcoxon_singed_rank_test_empty():
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
    estimator = WilcoxonSingedRankTest(alternative=alternative, type_ranking=type_ranking)

    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot be empty" in str(exc_info.value)


@pytest.mark.active
def test_wilcoxon_singed_rank_test_one_value():
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
    estimator = WilcoxonSingedRankTest(alternative=alternative, type_ranking=type_ranking)

    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt only one value" in str(exc_info.value)


@pytest.mark.active
def test_wilcoxon_singed_rank_test_nan_value():
    """
    This is our test to raise exception for series containing nanvalue
    """
    # Arrange
    numpy.random.seed(42)
    sample_size = 0

    a = numpy.empty((20))
    a[12:] = numpy.nan

    sample_0 = ToolsDataTest.from_array("dataset_0", "series_0", a)
    sample_1 = ToolsDataTest.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
    alternative = "greater"
    type_ranking = "unsafe"

    # Act
    estimator = WilcoxonSingedRankTest(alternative=alternative, type_ranking=type_ranking)

    with pytest.raises(Exception) as exc_info:
        #   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
        estimator.run(sample_0, sample_1)

    # Assert
    assert "series cannot containt nan or None values" in str(exc_info.value)


# @pytest.mark.broken
# def test_wilcoxon_singed_rank_test_constant_value():
#    """
#    This is our test to raise exception for series containing constant.
#    """
#    # Arrange
#    numpy.random.seed(42)
#    sample_size = 8
#    a = [1, 1, 1, 1, 1, 1, 1, 1]
#    a = numpy.array(a)
#    sample_0 = SeriesFederated.from_array("dataset_0", "series_0", a)
#    sample_1 = SeriesFederated.from_array("dataset_0", "series_0", numpy.random.normal(0, 1, sample_size))
#    alternative = "greater"
#    type_ranking = "unsafe"

# Act
#    estimator = WilcoxonSingedRankTest(alternative=alternative, type_ranking=type_ranking)

#    with pytest.raises(Exception) as exc_info:
#   pearson_sail, p_value_sail = estimator.run(sample_0, sample_1)
#        estimator.run(sample_0, sample_1)

# Assert
#    assert "input array is constant" in str(exc_info.value)

import pandas as pd
import pytest

from scipy.special import rel_entr
from sail_safe_functions_orchestrator.privacy.kl_divergence import kl_divergence


@pytest.mark.active
@pytest.mark.parametrize(
    "sample_0, sample_1",
    [([0.25, 0.33, 0.23, 0.19], [0.21, 0.21, 0.32, 0.26]), ([0.45, 0.23, 0.33, 0.69], [0.24, 0.18, 0.92, 0.56])],
)
def test_kl_divergence_forward(sample_0, sample_1):
    """
    Test for kl divergence
    """
    sample_0 = pd.Series(sample_0)
    sample_1 = pd.Series(sample_1)

    # Act
    estimator = kl_divergence()
    forward_value = estimator.run(sample_0, sample_1, False)

    scipy_forward_value = sum(rel_entr(sample_0, sample_1))

    # Assert
    assert scipy_forward_value == pytest.approx(forward_value, 0.0001)


@pytest.mark.active
@pytest.mark.parametrize(
    "sample_0, sample_1",
    [([0.25, 0.33, 0.23, 0.19], [0.21, 0.21, 0.32, 0.26]), ([0.45, 0.23, 0.33, 0.69], [0.24, 0.18, 0.92, 0.56])],
)
def test_kl_divergence_backward(sample_0, sample_1):
    """
    Test for kl divergence
    """
    # Arrange

    sample_0 = pd.Series(sample_0)
    sample_1 = pd.Series(sample_1)
    # Act
    estimator = kl_divergence()
    reverse_value = estimator.run(sample_0, sample_1, True)

    scipy_reverse_value = sum(rel_entr(sample_1, sample_0))

    # Assert
    assert scipy_reverse_value == pytest.approx(reverse_value, 0.0001)

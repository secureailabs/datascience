import pandas as pd
import pytest

from scipy.special import rel_entr
from sail_safe_functions_orchestrator.privacy.kl_divergence import kl_divergence


@pytest.mark.active
def test_kl_divergence():
    """
    Test for kl divergence
    """
    # Arrange
    sample_0 = [0.25, 0.33, 0.23, 0.19]
    sample_1 = [0.21, 0.21, 0.32, 0.26]

    sample_0 = pd.Series(sample_0)
    sample_1 = pd.Series(sample_1)
    # Act
    estimator = kl_divergence()
    forward_value = estimator.run(sample_0, sample_1, False)

    scipy_forward_value = sum(rel_entr(sample_0, sample_1))

    # Assert
    assert scipy_forward_value == pytest.approx(forward_value, 0.0001)

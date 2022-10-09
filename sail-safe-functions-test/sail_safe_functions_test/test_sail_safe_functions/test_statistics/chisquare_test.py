from typing import List, Tuple

import pandas as pd
import pytest
from sail_safe_functions_orchestrator.statistics import chisquare, chisquare_local

# @pytest.mark.active
# def test_chisquare_direct(
#     two_sample_categorical: Tuple[SeriesFederatedLocal, SeriesFederatedLocal],
# ):
#     """
#     This is our test for the Sails federated chisquare test

#     :param two_sample_categorical a dataset with cathegorical data
#     :type two_sample_categorical: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
#     """
#     # Arrange
#     sample_0 = two_sample_categorical[0]
#     sample_1 = two_sample_categorical[1]

#     # Act
#     statistics.chisquare(sample_0, sample_1)


@pytest.mark.active
def test_chisquare(
    connect_to_one_VM,
    two_sample_categorical_remote: Tuple[List, List],
    two_sample_categorical_local: Tuple[pd.Series, pd.Series],
):
    """
    This is our test for the Sails federated chisquare test

    :param two_sample_categorical a dataset with cathegorical data
    :type two_sample_categorical: Tuple[SeriesFederatedLocal, SeriesFederatedLocal]
    """
    # Arrange
    sample_0_remote = two_sample_categorical_remote[0]
    sample_1_remote = two_sample_categorical_remote[1]
    sample_0_local = two_sample_categorical_local[0]
    sample_1_local = two_sample_categorical_local[1]
    clients = [connect_to_one_VM]

    # Act
    pearson_sail, p_value_sail = chisquare(clients, sample_0_remote, sample_1_remote)
    pearson_scipy, p_value_scipy = chisquare_local(sample_0_local, sample_1_local)

    # Assert
    assert pearson_scipy == pytest.approx(pearson_sail, 0.0001)
    assert p_value_scipy == pytest.approx(p_value_sail, 0.0001)

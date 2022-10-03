import pytest
from sail_orchestrator_lib.statistics import kolmogorov_smirnov, kolmogorov_smirnov_local


@pytest.mark.active
def test_kolmogorov_smirnov_normalunit(
    connect_to_one_VM,
    one_sample_normal_remote,
    one_sample_normal_local,
):
    """Preform a kolmogorov_smirnov test for normality"""
    sample_0_remote = one_sample_normal_remote
    sample_0_local = one_sample_normal_local
    clients = [connect_to_one_VM]

    # Act
    k_statistic_sail, p_value_sail = kolmogorov_smirnov(
        clients,
        sample_0_remote,
        type_distribution="normalunit",
    )
    k_statistic_scipy, p_value_scipy = kolmogorov_smirnov_local(sample_0_local, type_distribution="normalunit")

    # Assert
    assert k_statistic_sail == pytest.approx(k_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)

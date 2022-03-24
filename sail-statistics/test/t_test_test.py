import pytest

from scipy import stats

from sail_statstics.local_federated_dataframe import LocalFederatedDataframe
from sail_statstics.procedure.t_test.t_test_federate import TTestFederate


@pytest.mark.active
def test_t_test():
    # Arrange
    list_path_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
    id_column_0 = "PD-L1 level before treatment"
    id_column_1 = "PD-L1 level after treatment"

    dataframe = LocalFederatedDataframe()
    for path_file_csv in list_path_file_csv:
        dataframe.add_csv(path_file_csv)

    sample_0 = dataframe[id_column_0]
    sample_1 = dataframe[id_column_1]

    sample_0_numpy = dataframe[id_column_0].to_numpy()
    sample_1_numpy = dataframe[id_column_1].to_numpy()

    # Act
    t_statistic_sail, p_value_sail = TTestFederate.ttest_ind(sample_0, sample_1, equal_var=True, alternative="less")

    t_statistic_scipy, p_value_scipy = stats.ttest_ind(
        sample_0_numpy, sample_1_numpy, equal_var=True, alternative="less"
    )

    # Assert
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)

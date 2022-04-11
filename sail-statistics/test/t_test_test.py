import pytest
import numpy as np
from scipy import stats

from sail_statstics.local_federated_dataframe import LocalFederatedDataframe
from sail_statstics.procedure.t_test.t_test_federate import TTestFederate


@pytest.mark.active
def test_t_test_unpaired_equal_varriance():
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
    t_statistic_sail, p_value_sail = TTestFederate.ttest_ind(
        sample_0, sample_1, equal_varriances=True, alternative="less"
    )

    t_statistic_scipy, p_value_scipy = stats.ttest_ind(
        sample_0_numpy, sample_1_numpy, equal_var=True, alternative="less"
    )

    # Assert
    # TODO Can we remove these print statement
    # print(t_statistic_sail)
    # print(p_value_sail)
    # print(t_statistic_scipy)
    # print(p_value_scipy)

    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)


@pytest.mark.active
def test_t_test_unpaired_unequal_varriance_small():
    sample_0_numpy = np.array([17.2, 20.9, 22.6, 18.1, 21.7, 21.4, 23.5, 24.2, 14.7, 21.8])
    sample_1_numpy = np.array(
        [
            21.5,
            22.8,
            21.0,
            23.0,
            21.6,
            23.6,
            22.5,
            20.7,
            23.4,
            21.8,
            20.7,
            21.7,
            21.5,
            22.5,
            23.6,
            21.5,
            22.5,
            23.5,
            21.5,
            21.8,
        ]
    )

    sample_0 = LocalFederatedDataframe()
    sample_1 = LocalFederatedDataframe()
    sample_0.add_array("frame_test", "PD-L1 level before treatment", sample_0_numpy)
    sample_1.add_array("frame_test", "PD-L1 level after treatment", sample_1_numpy)
    t_statistic_sail, p_value_sail = TTestFederate.ttest_ind(
        sample_0, sample_1, equal_varriances=False, alternative="less"
    )

    t_statistic_scipy, p_value_scipy = stats.ttest_ind(
        sample_0_numpy, sample_1_numpy, equal_var=False, alternative="less"
    )

    # Assert
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)


@pytest.mark.active
def test_t_test_unpaired_unequal_varriance():
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
    t_statistic_sail, p_value_sail = TTestFederate.ttest_ind(
        sample_0, sample_1, equal_varriances=False, alternative="less"
    )

    t_statistic_scipy, p_value_scipy = stats.ttest_ind(
        sample_0_numpy, sample_1_numpy, equal_var=False, alternative="less"
    )

    # Assert
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)

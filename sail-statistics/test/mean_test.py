import pytest
import numpy as np
from scipy import stats

from sail_statstics.local_federated_dataframe import LocalFederatedDataframe
from sail_statstics.procedure.mean.mean_federate import MeanFederate


@pytest.mark.active
def test_mean():
    # Arrange
    list_path_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
    id_column_0 = "PD-L1 level before treatment"

    dataframe = LocalFederatedDataframe()
    for path_file_csv in list_path_file_csv:
        dataframe.add_csv(path_file_csv)

    sample_0 = dataframe[id_column_0]
    sample_0_numpy = dataframe[id_column_0].to_numpy()

    # Act
    mean_sail = MeanFederate.mean(sample_0)
    mean_numpy = np.mean(sample_0_numpy)

    # Assert
    assert mean_sail == pytest.approx(mean_numpy, 0.0001)

import numpy
from sail_safe_functions_orchestrator import statistics
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.statistics.estimator import Estimator


def covariance_matrix(data_frame: DataFrameFederated) -> numpy.ndarray:
    """
    covariance_matrix is defined as the matrix of all covariance

    :param sample_0: sample_0
    :type sample_0: SeriesFederated
    :param sample_1: sample_1
    :type sample_1: SeriesFederated
    :return: covariance_matrix value

    """
    estimator = CovarianceMatrix()
    return estimator.run(data_frame)


class CovarianceMatrix(Estimator):
    """
    Estimator for covariance_matrix
    """

    def __init__(self) -> None:
        super().__init__(["covariance_matrix"])

    def run(self, data_frame: DataFrameFederated) -> numpy.ndarray:
        list_precompute = []
        list_name_column = data_frame.columns
        count_series = len(list_name_column)
        array_covariance_matrix = numpy.zeros((count_series, count_series))
        for i in range(count_series):
            for j in range(i, count_series):
                covariance = statistics.covariance(data_frame[list_name_column[i]], data_frame[list_name_column[j]])
                array_covariance_matrix[i, j] = covariance
                array_covariance_matrix[j, i] = covariance
        return array_covariance_matrix

    def run_reference(self, data_frame: DataFrameFederated) -> numpy.ndarray:
        array = data_frame.to_numpy().astype(numpy.float64)
        return numpy.cov(array.T)

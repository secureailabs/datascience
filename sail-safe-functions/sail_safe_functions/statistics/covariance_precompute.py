from typing import Dict

import pandas
from sail_safe_functions.common.tool_moment import compute_dict_geometric_moment


class CovariancePrecompute(object):
    """
    This class it get the precomputes required for the covariance

    :param object:
    :type object:
    """

    def run(sample_0: pandas.Series, sample_1: pandas.Series) -> Dict[str, float]:
        """
        Parameters
        ----------
        sample_0_dataframe : pd.DataFrame
            The dataframe for sample_0

        sample_1_dataframe : pd.DataFrame
            The dataframe for sample_1

        Returns
        -------
        a list of 6 floats
        """
        sample_0 = sample_0.astype(float)
        sample_1 = sample_1.astype(float)
        list_series = [sample_0, sample_1]
        list_code_moment = []
        list_code_moment.append("0_0")
        list_code_moment.append("0_0")
        list_code_moment.append("0_1")
        list_code_moment.append("1_0")
        list_code_moment.append("1_1")
        list_code_moment.append("0_1_1_1")

        return compute_dict_geometric_moment(list_series, list_code_moment)

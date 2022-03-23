from scipy import stats
import numpy as np
from scipy.stats import t
import pandas as pd
import pytest 
#from assertpy.assertpy import assert_that

from sail_statstics.procedure.t_test_precompute import TTestPrecompute
from sail_statstics.procedure.t_test_agregate import TTestAgregate

#
# This test follows https://en.wikipedia.org/w/index.php?title=Welch%27s_t-test&oldid=994214781#Examples
# Example 1
#
#sample_0 = np.array([27.5, 21.0, 19.0, 23.6, 17.0, 17.9, 16.9, 20.1, 21.9, 22.6, 23.1, 19.6, 19.0, 21.7, 21.4])
#sample_1 = np.array([27.1, 22.0, 20.8, 23.4, 23.4, 23.5, 25.8, 22.0, 24.8, 20.2, 21.9, 22.1, 22.9, 20.5, 24.4])

@pytest.mark.active
def test_match_scipy():
    # Arrange
    list_path_file = ['bmc1.csv', 'bwh1.csv', 'mgh1.csv']
    id_column_0 = 'PD-L1 level before treatment'
    id_column_1 = 'PD-L1 level after treatment'
    list_sample_0 = []
    list_sample_1 = []
    for path_file in list_path_file:
        list_sample_0.append(pd.read_csv(path_file)[id_column_0].to_numpy())
        list_sample_1.append(pd.read_csv(path_file)[id_column_1].to_numpy())

    sample_0_full = np.concatenate(list_sample_0)
    sample_1_full = np.concatenate(list_sample_1)

    # Act
    list_list_precompute = []
    for sample_0, sample_1 in zip(list_sample_0, list_sample_1): 
        list_list_precompute.append(TTestPrecompute.run(sample_0, sample_1))
    t_statistic_sail, degrees_of_freedom = TTestAgregate.run(list_list_precompute)
    p_value_sail = t.cdf(t_statistic_sail, degrees_of_freedom)



    t_statistic_scipy, p_value_scipy = stats.ttest_ind(sample_0_full, sample_1_full, equal_var=True, alternative='less')
    # Assert
    
    assert t_statistic_sail == pytest.approx(t_statistic_scipy, 0.0001)
    assert p_value_sail == pytest.approx(p_value_scipy, 0.0001)

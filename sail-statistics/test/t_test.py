from scipy import stats
import numpy as np
from scipy.stats import t

from sail_statstics.procedure.t_test_precompute import TTestPrecompute
from sail_statstics.procedure.t_test_agregate import TTestAgregate

#
# This test follows https://en.wikipedia.org/w/index.php?title=Welch%27s_t-test&oldid=994214781#Examples
# Example 1
#

sample_0 = np.array([27.5, 21.0, 19.0, 23.6, 17.0, 17.9, 16.9, 20.1, 21.9, 22.6, 23.1, 19.6, 19.0, 21.7, 21.4])
sample_1 = np.array([27.1, 22.0, 20.8, 23.4, 23.4, 23.5, 25.8, 22.0, 24.8, 20.2, 21.9, 22.1, 22.9, 20.5, 24.4])

list_precompute_0 = TTestPrecompute.run(sample_0, sample_1)
list_list_precompute = [list_precompute_0]
t_statistic, degrees_of_freedom = TTestAgregate.run(list_list_precompute)
p_value = t.cdf(t_statistic, degrees_of_freedom)
print('')
print('via sail')
print('t_statistic: ' + str(t_statistic))
print('p_value: ' + str(p_value))

t_statistic, p_value = stats.ttest_ind(sample_0, sample_1, equal_var=True, alternative='less')
print('')
print('via scipy')
print('t_statistic: ' + str(t_statistic))
print('p_value: ' + str(p_value))

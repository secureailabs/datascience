from typing import List

from sail_core.implementation_manager import ImplementationManager
from sail_safe_functions.test.helper_sail_safe_functions.participant_service_local import ParticipantSeriviceLocal

implementation_manager = ImplementationManager.get_instance()
if not implementation_manager.is_initialized:
    implementation_manager.set_participant_service(ParticipantSeriviceLocal())
    implementation_manager.initialize()

import os

# load every test dataset
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.series_federated import SeriesFederated
from sail_safe_functions.test.helper_sail_safe_functions.tools_data_test import ToolsDataTest
from sail_safe_functions.test.test_sail_safe_functions.conftest import (
    load_cardio,
    load_gdc_941_1,
    load_house,
    load_investor,
    load_kidney_clean,
)

list_series_number: List[SeriesFederated] = []
data_path = os.environ["PATH_SAIL_TEST_DATA"]
list_data_frame = []
list_data_frame.append(load_kidney_clean(data_path))
list_data_frame.append(load_investor(data_path))
list_data_frame.append(load_house(data_path))
list_data_frame.append(load_cardio(data_path))
list_data_frame.append(load_gdc_941_1(data_path))


for data_frame in list_data_frame:
    for series_name in data_frame.list_series_name:
        series = data_frame[series_name]
        if series.data_model_series.type_data_level == DataModelSeries.DataLevelInterval:
            list_series_number.append(series)


import numpy
from sail_safe_functions.aggregator import preprocessing, statistics

# TODO create a function to drop nans in a series
for series in list_series_number:

    print(series.series_name)
    if numpy.isnan(series.to_numpy()).any():
        print("has nan")
        continue
    # print(series.to_numpy())
    print(statistics.min_max(series))

    preprocessing.cumulative_distribution_function(series)
#     domain_min, domain_max = statistics.min_max(series)
#     list_precompute = series.map_function(CumulativeDistributionFunctionPrecompute, domain_min, domain_max)
#     result = preprocessing.cumulative_distribution_function(series)

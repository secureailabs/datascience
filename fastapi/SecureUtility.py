##################################################
# This file contains the validation code for ensuring data is of appropriate length.
# Will contain more in time.
##################################################
# Property of Secure AI Labs
##################################################
# Author: Adam J. Hall
# Copyright: Copyright 02/11/2022, MVP Delivery
# Version: 0.0.0
# Maintainer: Secure AI Labs
# Email: adam.hall@secureailabs.com
# Status: Alpha
##################################################

from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import (
    DataFrameFederatedLocal,
)
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import (
    SeriesFederatedLocal,
)
import os

from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.dataset_longitudinal_federated import (
    DatasetLongitudinalFederated,
)


def dataset_longitudinal_r4sep2019_1k_3() -> DatasetLongitudinalFederated:
    DATA_PATH = (
        "../sail-safe-functions-test/sail_safe_functions_test/data_sail_safe_functions"
    )
    path_file_data_federation = os.path.join(
        DATA_PATH, "data_federation_packaged", "r4sep2019_fhirv1_1k_3.zip"
    )
    return DatasetLongitudinalFederated.read_for_path_file(path_file_data_federation)


def data_frame_federated_kidney() -> DataFrameFederated:
    """
    Fixture for loading a dataframe with missing values
    :return: data_frame_federated_kidney: a federated dataframe
    :rtype: class : DataFrameFederatedLocal
    """
    DATA_PATH = (
        "../sail-safe-functions-test/sail_safe_functions_test/data_sail_safe_functions"
    )

    list_name_file_csv = ["kidney_disease_clean.csv"]
    id_column_0 = "PD-L1 level before treatment"

    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_kidney_clean", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    return DataFrameFederatedLocal.from_csv(dict_csv)


def get_series() -> SeriesFederated:
    """
    Temporary Function for getting data

    :return: sample series
    :type: sample remote series
    """
    return two_sample_big()[0]


def get_series_different() -> SeriesFederated:
    """
    Temporary Function for getting data

    :return: sample series
    :type: sample remote series
    """
    return two_sample_big()[1]


def two_sample_big() -> SeriesFederatedLocal:
    """
    Fixture for SeriesFederatedLocal with this first part of the investor demo dataset

    :return: DataFrameFederatedLocal
    :rtype: class : test_sail_safe_functions.series_federated_local.SeriesFederatedLocal
    """
    DATA_PATH = (
        "../sail-safe-functions-test/sail_safe_functions_test/data_sail_safe_functions"
    )

    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]
    id_column_0 = "PD-L1 level before treatment"
    id_column_1 = "PD-L1 level after treatment"

    dict_csv = {}
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_investor_demo", name_file_csv)
        dict_csv[name_file_csv] = path_file_csv
    data_frame = DataFrameFederatedLocal.from_csv(dict_csv)

    return (data_frame[id_column_0], data_frame[id_column_1])


def query_limit_n(data, n=10) -> bool:
    """
    Checks data or series in question is over a given threshold.

    :param: data: the data item being checked
    :type: remote dataframe or remote series
    :return: True or False relating to whether the threshold has been surpassed
    :type: Boolean
    """
    return data.global_row_count() > n


def validate(data) -> bool:
    """
    Validates execution criteria for data inputs
    :param: data: the data item being validated
    :type: Remote Dataframe or Remote Series
    :return: sample series
    :type: Error message or True condition depending on whether validation passes
    """

    # Check query limit N
    if not query_limit_n(data):
        return {"payload": "Error: Federation Length Too Small"}
    else:
        return True

    # CHECKS
    # TODO:
    #       1. Check for pandas query injection in column_id string
    # CLOSE CHECKS

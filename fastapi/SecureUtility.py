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
import os


def get_dataframe():
    """
    Temporary Function for getting data

    :return: sample dataframe
    :type: remote dataframe
    """
    DATA_PATH = (
        "../sail-safe-functions-test/sail_safe_functions_test/data_sail_safe_functions"
    )

    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]

    dataframe = DataFrameFederatedLocal()
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_investor_demo", name_file_csv)
        dataframe.add_csv(path_file_csv)
    return dataframe


def get_series():
    """
    Temporary Function for getting data

    :return: sample series
    :type: sample remote series
    """
    dataframe = get_dataframe()
    series = dataframe["PD-L1 level before treatment"]
    return series


def get_series_different():
    """
    Temporary Function for getting data

    :return: sample series
    :type: sample remote series
    """
    dataframe = get_dataframe()
    series = dataframe["PD-L1 level after treatment"]
    return series


def query_limit_n(data, n=10):
    """
    Checks data or series in question is over a given threshold.

    :param: data: the data item being checked
    :type: remote dataframe or remote series
    :return: True or False relating to whether the threshold has been surpassed
    :type: Boolean
    """
    return data.global_row_count() > n


def validate(data):
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

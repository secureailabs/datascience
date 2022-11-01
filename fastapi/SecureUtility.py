from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import (
    DataFrameFederatedLocal,
)
import os


def get_dataframe():
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
    dataframe = get_dataframe()
    series = dataframe["PD-L1 level before treatment"]
    return series


def query_limit_n(data, n=10):
    return data.global_row_count() > n


def validate(data):
    # Check query limit N
    if not query_limit_n(data):
        return {"payload": "Error: Federation Length Too Small"}
    else:
        return data

    # CHECKS
    # TODO:
    #       1. Check for pandas query injection in column_id string
    # CLOSE CHECKS

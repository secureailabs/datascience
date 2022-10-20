from fastapi import FastAPI
from sail_safe_functions_orchestrator.statistics.mean import Mean
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import (
    DataFrameFederatedLocal,
)
import os

app = FastAPI()


def get_data():
    DATA_PATH = (
        "../sail-safe-functions-test/sail_safe_functions_test/data_sail_safe_functions"
    )

    list_name_file_csv = ["bmc1.csv", "bwh1.csv", "mgh1.csv"]

    dataframe = DataFrameFederatedLocal()
    for name_file_csv in list_name_file_csv:
        path_file_csv = os.path.join(DATA_PATH, "data_csv_investor_demo", name_file_csv)
        dataframe.add_csv(path_file_csv)
    return dataframe


def query_limit_n(data, n=10):
    return data.global_row_count() > n


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/mean")
async def mean(dataframe_uuid: str, column_id: str):

    # CHECK DATAFRAME EXISTS
    # TODO: Link this into checking the store for accessible data.
    #       This functionality is not available right now but should be after the system comes together.
    if dataframe_uuid == "UUID":
        dataframe = get_data()
    else:
        return {"payload": "Error: Federation UUID not found"}

    # CHECK DATAFRAME IS LONG ENOUGH
    if not query_limit_n(dataframe):
        return {"payload": "Error: Federation Length Too Small"}

    # Return Mean Result
    federated_series = dataframe[column_id]
    estimator = Mean()
    mean_sail = estimator.run(federated_series)
    return {"payload": mean_sail}

    # CHECKS
    # TODO:
    #       1. Check for pandas query injection in column_id string
    # CLOSE CHECKS


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

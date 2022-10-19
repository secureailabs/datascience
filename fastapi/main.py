from fastapi import FastAPI
from sail_safe_functions_orchestrator.statistics.mean import Mean
from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import (
    DataFrameFederatedLocal,
)
import os


from sail_safe_functions_test.helper_sail_safe_functions.data_frame_federated_local import (
    DataFrameFederatedLocal,
)

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/mean")
async def mean(dataframe_uuid: str, column_id: str):

    # BEGIN CHECKS
    # TODO:
    #       1. Implement input validation / safety checks
    #           1a. Check for pandas query injection in column_id string
    #           1b. Check query limit N on federated series
    #           1c. Check dataset UUID exists
    # CLOSE CHECKS

    if dataframe_uuid == "UUID":
        dataframe = get_data()
        federated_series = dataframe[column_id]
        estimator = Mean()
        mean_sail = estimator.run(federated_series)
        return {"mean": mean_sail}
    else:
        return {"mean": "Error: Federation UUID not found"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

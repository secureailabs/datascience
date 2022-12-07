from fastapi import APIRouter
from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_test.helper_sail_safe_functions.test_service_reference import TestServiceReference

router = APIRouter()


# DATA MODEL


@app.post("/data_model/new_tabular_model")
async def data_frame_tabular() -> dict:
    data_frame_tabular = DataModelTabular()
    data_frame_id = service_reference.get_instance().data_model_tabular_to_reference(data_frame_tabular)

    return {"data_frame_tabular_id": data_frame_id}


@app.post("/data_model/new_series_model_numerical")
async def new_series_numerical(series_name: str, measurement_source_name: str, type_agregator: str, unit: str) -> dict:

    series = DataModelSeries.create_numerical(
        series_name=series_name,
        measurement_source_name=measurement_source_name,
        type_agregator=type_agregator,
        unit=unit,
    )
    series_ref = service_reference.get_instance().data_model_series_to_reference(series)

    return {"series": series_ref}


@app.post("/data_model/tabular/{data_model_tabular_id}/add_dataframe")
async def tabular_model_add_dataframe_model(data_model_tabular_id: str, data_model_dataframe_id: str) -> dict:
    data_model_tabular = service_reference.get_instance().reference_to_data_model_tabular(data_model_tabular_id)
    data_model = service_reference.get_instance().reference_to_data_model_data_frame(data_model_dataframe_id)

    data_model_tabular.add_data_model_data_frame(data_model)

    return {"data_frame_tabular_id": data_model_tabular_id}


@app.post("/data_model/new_data_frame_model")
async def create_data_model_data_frame(data_frame_name: str) -> dict:
    dataframe_id = ""
    if data_frame_name not in dataframe_name_lookup:
        new_dataframe = DataModelDataFrame(data_frame_name)
        dataframe_id = service_reference.get_instance().data_model_data_frame_to_reference(new_dataframe)
        dataframe_name_lookup[data_frame_name] = dataframe_id
    else:
        dataframe_id = dataframe_name_lookup[data_frame_name]

    return {"data_model_id": dataframe_id}


@app.post("/data_model/data_frame/{data_model_id}/add_new_series_model")
async def data_model_add_series_model(
    data_model_id: str,
    series_name: str,
    measurement_source_name: str,
    type_agregator: str,
) -> dict:
    data_model_data_frame = service_reference.get_instance().reference_to_data_model_data_frame(data_model_id)
    if data_model_data_frame is not None:
        data_model_data_frame.add_data_model_series(
            DataModelSeries.create_numerical(
                series_name=series_name,
                measurement_source_name=measurement_source_name,
                type_agregator=type_agregator,
                unit="kg/m2",
            )
        )

    return {"data_model_id": data_model_id}


# DATA MODEL END

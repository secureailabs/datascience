
from fastapi import Body, Depends, FastAPI, HTTPException, Path, Response, status
from fastapi import APIRouter
from sail_safe_functions.test.helper_sail_safe_functions.test_service_reference import TestServiceReference
from sail_safe_functions.aggregator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions.aggregator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.aggregator.data_model.data_model_tabular import DataModelTabular

router = APIRouter(
    prefix='/data_model',
    tags = ['Data Model Functionality']
)

# DATA MODEL
service_reference = TestServiceReference.get_instance()

@router.post(
    path="/new_data_frame_tabular/",
    description="Create new Tabular Data Model",
    response_description="Reference to generated tabular data model",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="new_tabular_model",
)
async def new_data_frame_tabular() -> dict:
    data_frame_tabular = DataModelTabular()
    data_frame_id = service_reference.get_instance().data_model_tabular_to_reference(data_frame_tabular)

    return {"data_frame_tabular_id": data_frame_id}


@router.post(
    path="/new_series_model_numerical",
    description="Create new numerical Series Model",
    response_description="Reference to generated numerical Series Model",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="new_series_model_numerical",
)
async def new_series_model_numerical(
    series_name: str = Body(description="name of the series"),
    measurement_source_name: str = Body(description="Source featuree of the series."),
    type_agregator: str = Body(description="Method by which source of data is to be aggregated"),
    unit: str = Body(description="The unit type of the series model"),
) -> dict:
    series = DataModelSeries.create_numerical(
        series_name=series_name,
        measurement_source_name=measurement_source_name,
        type_agregator=type_agregator,
        unit=unit,
    )
    series_id = service_reference.get_instance().data_model_series_to_reference(series)

    return {"series_id": series_id}


@router.post(
    path="/data_model_tabular_add_dataframe",
    description="Add a Dataframe model to a Tabular Dataframe Model",
    response_description="Reference to Tabular Dataframe Model",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="tabular_model_add_dataframe_model",
)
async def tabular_model_add_dataframe_model(
    data_model_tabular_id: str = Body(description="The reference to the Tabular Dataframe model being added to."),
    data_model_dataframe_id: str = Body(
        description="The reference to the Dataframe model being added to the Tabular Dataframe."
    ),
) -> dict:
    data_model_tabular = service_reference.get_instance().reference_to_data_model_tabular(data_model_tabular_id)
    data_model = service_reference.get_instance().reference_to_data_model_data_frame(data_model_dataframe_id)

    data_model_tabular.add_data_model_data_frame(data_model)

    return {"data_frame_tabular_id": data_model_tabular_id}


@router.post(
    path="/new_data_model_data_frame",
    description="Create a new Dataframe model.",
    response_description="Reference to Dataframe model",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="new_data_model_data_frame",
)
async def new_data_model_data_frame(
    data_frame_name: str = Body(description="Desired name of the new Dataframe"),
) -> dict:
    dataframe_id = ""
    if data_frame_name not in dataframe_name_lookup:
        new_dataframe = DataModelDataFrame(data_frame_name)
        dataframe_id = service_reference.get_instance().data_model_data_frame_to_reference(new_dataframe)
        dataframe_name_lookup[data_frame_name] = dataframe_id
    else:
        dataframe_id = dataframe_name_lookup[data_frame_name]

    return {"data_model_id": dataframe_id}


@router.post(
    path="/dataframe_model_add_new_series_model.",
    description="Create a new numerical series model and add it to a Dataframe model.",
    response_description="Reference to Dataframe model.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="dataframe_model_add_new_series_model",
)
async def dataframe_model_add_series_model(
    data_model_id: str = Body(description="Reference to the data model being added to."),
    series_name: str = Body(description="Name of the new series model to be added."),
    measurement_source_name: str = Body(description="The feature to aggregate."),
    type_agregator: str = Body(description="Method by which source of data is to be aggregated for new series model"),
    unit: str = Body(description="The unit of measurement of the new series to be added."),
) -> dict:
    data_model_data_frame = service_reference.get_instance().reference_to_data_model_data_frame(data_model_id)
    if data_model_data_frame is not None:
        data_model_data_frame.add_data_model_series(
            DataModelSeries.create_numerical(
                series_name=series_name,
                measurement_source_name=measurement_source_name,
                type_agregator=type_agregator,
                unit=unit,
            )
        )

    return {"data_model_id": data_model_id}


# DATA MODEL END


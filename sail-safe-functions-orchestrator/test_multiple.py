from sail_safe_functions.preprocessing.read_dataset_fhirv1 import ReadZipJsonFhirPrecompute

from sail_safe_functions_orchestrator import preprocessing
from sail_safe_functions_orchestrator.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.data_model_tabular import DataModelDataFrame

path_dir_source = "/home/jaap/data/data_zipjsonfhir_r4sep2019_20_1"
path_dir_target = "/home/jaap/data/data_csv_r4sep2019_20_1"


preprocessing.read_zip_json_fhir(path_dir_source)

data_model_data_frame = DataModelDataFrame()
data_model_data_frame.add_data_model_series(
    DataModelSeries.create_numerical(
        series_name="bmi_mean",
        measurement_source_name="Observation:Body Mass Index",
        type_agregator=DataModelSeries.AgregatorIntervalMean,
    )
)
data_model_data_frame.add_data_model_series(
    DataModelSeries.create_numerical(
        series_name="bmi_first",
        measurement_source_name="Observation:Body Mass Index",
        type_agregator=DataModelSeries.AgregatorIntervalFirstOccurance,
    )
)

data_model_data_frame.add_data_model_series(
    DataModelSeries.create_numerical(
        series_name="bmi_last",
        measurement_source_name="Observation:Body Mass Index",
        type_agregator=DataModelSeries.AgregatorIntervalLastOccurance,
    )
)
data_frame_table = data_frame_longitudinal.convert_to_data_frame_table(data_model_data_frame)
data_frame_table.to_csv(path_file_target)

from sail_safe_functions.preprocessing.read_dataset_fhirv1 import ReadDatasetFhirv1Precompute

from sail_safe_functions_orchestrator.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.data_model_tabular import DataModelTabular

path_file_source = "/home/jaap/data/data_zipjsonfhir_r4sep2019_20_1/dataset_0.zip"
path_file_target = "/home/jaap/data/cohort_0.csv"

data_frame_longitudinal = ReadDatasetFhirv1Precompute.run(path_file_source)
# print(data_frame.head())
# data_frame_longitudinal.print_at_least_one()


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

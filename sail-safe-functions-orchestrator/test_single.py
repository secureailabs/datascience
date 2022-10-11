from sail_safe_functions.preprocessing.read_zip_json_fhir_precompute import ReadZipJsonFhirPrecompute

from sail_safe_functions_orchestrator.data_model_feature import DataModelFeature
from sail_safe_functions_orchestrator.data_model_table import DataModelTable

path_file_source = "/home/jaap/data/data_zipjsonfhir_r4sep2019_20_1/dataset_0.zip"
path_file_target = "/home/jaap/data/cohort_0.csv"

data_frame_logitudinal = ReadZipJsonFhirPrecompute.run(path_file_source)
# print(data_frame.head())
# data_frame_logitudinal.print_at_least_one()


data_model_table = DataModelTable()
data_model_table.add_data_model_feature(
    DataModelFeature.create_numerical(
        feature_name="bmi_mean",
        measurement_source_name="Observation:Body Mass Index",
        type_agregator=DataModelFeature.AgregatorIntervalMean,
    )
)
data_model_table.add_data_model_feature(
    DataModelFeature.create_numerical(
        feature_name="bmi_first",
        measurement_source_name="Observation:Body Mass Index",
        type_agregator=DataModelFeature.AgregatorIntervalFirstOccurance,
    )
)

data_model_table.add_data_model_feature(
    DataModelFeature.create_numerical(
        feature_name="bmi_last",
        measurement_source_name="Observation:Body Mass Index",
        type_agregator=DataModelFeature.AgregatorIntervalLastOccurance,
    )
)
data_frame_table = data_frame_logitudinal.convert_to_data_frame_table(data_model_table)
data_frame_table.to_csv(path_file_target)

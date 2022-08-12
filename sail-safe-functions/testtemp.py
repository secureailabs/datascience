from sail_safe_functions.preprocessing.ingest_json import IngestJsonZip

path_file_source = "/home/jaap/data/synthea_sample_data_fhir_r4_sep2019.zip"
path_file_target = "/home/jaap/data/cohort_0.csv"

dict_feature_template = IngestJsonZip.temp_create_dict_feature_template()
data_frame = IngestJsonZip.run(path_file_source, dict_feature_template)
print(data_frame.head())
data_frame.to_csv(path_file_target)

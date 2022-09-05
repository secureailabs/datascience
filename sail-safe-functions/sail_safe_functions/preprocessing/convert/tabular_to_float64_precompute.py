import numpy
import pandas
from sail_safe_functions.preprocessing.convert.categorical_to_onehot import CategoricalToOnehot
from sail_safe_functions_orchestrator.schema_date_frame import SchemaDataFrame
from sail_safe_functions_orchestrator.schema_feature import SchemaFeature


class TabularToFloat64Precompute:
    def run(schema_data_frame: SchemaDataFrame, data_frame_source: pandas.DataFrame) -> pandas.DataFrame:
        if len(schema_data_frame.list_name_feature) == 0:
            raise Exception("schema_data_frame must contain at least 1 schema_feature")
        # TODO check schema against data_frame or integrate it
        list_data_frame_target = []
        for feature_name in schema_data_frame.list_name_feature:
            schema_feature = schema_data_frame.get_schema_feature[feature_name]

            if schema_feature.data_level == SchemaFeature.DataLevelUnique:
                pass
            elif schema_feature.data_level == SchemaFeature.DataLevelCategorical:
                list_data_frame_target.append(CategoricalToOnehot.run(schema_feature, data_frame_source))
            elif schema_feature.data_level == SchemaFeature.DataLevelInterval:
                list_data_frame_target.append(data_frame_source[schema_feature].astype(numpy.float64).to_frame())

        return pandas.concat(list_data_frame_target, axis=1)

import numpy
import pandas
from sail_safe_functions_orchestrator.schema_feature import SchemaFeature


class CategoricalToOnehot:
    def run(schema_feature: SchemaFeature, data_frame_source: pandas.DataFrame) -> pandas.DataFrame:
        feature_name = schema_feature.feature_name
        type_missing_policy = schema_feature.missing_policy

        if type_missing_policy == schema_feature.MissingPolicyPropagateAddColumn:
            dummy_na = True
        else:
            dummy_na = False

        if type_missing_policy == schema_feature.MissingPolicyRaiseException:
            if 0 < data_frame_source[feature_name].isna().sum():
                raise ValueError(f"Column {feature_name} contains expeption while not should be present")

        data_frame_target = pandas.get_dummies(
            data_frame_source[feature_name],
            prefix=feature_name,
            prefix_sep="_",
            dummy_na=dummy_na,
            columns=schema_feature.list_value,
            sparse=False,
            drop_first=False,
            dtype=numpy.float64,
        )
        return data_frame_target

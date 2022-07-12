import numpy
import pandas
from sail_safe_functions.preprocessing.convert.categorical_to_onehot import CategoricalToOnehot


class TabularToFloat64:
    def run(table_schema: dict, data_frame_source: pandas.DataFrame) -> pandas.DataFrame:

        list_data_frame_target = []
        for name_column in data_frame_source.columns:
            column_schema = table_schema["dict_column"][name_column]

            if column_schema["type_data_level"] == "unique":
                pass
            elif column_schema["type_data_level"] == "categorical":
                list_data_frame_target.append(CategoricalToOnehot.run(column_schema, data_frame_source))
            elif column_schema["type_data_level"] == "interval":
                list_data_frame_target.append(data_frame_source[name_column].astype(numpy.float64).to_frame())

        return pandas.concat(list_data_frame_target, axis=1)

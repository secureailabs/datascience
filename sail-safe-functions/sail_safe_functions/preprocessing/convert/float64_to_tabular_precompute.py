import pandas
from sail_safe_functions.preprocessing.convert.onehot_to_categorical import (
    OnehotToCategorical,
)


class Float64ToTabularPrecompute:
    def run(table_schema: dict, data_frame_source: pandas.DataFrame) -> pandas.DataFrame:
        """
        Convert dtype float64 to tabular

            :type table_schema: dict
            :param data_frame_source: datafrane source
            :type data_frame_source: pandas.DataFrame
            :return: return tabular precompute
            :rtype: pandas.DataFrame
        """
        list_data_frame_target = []
        for name_column in table_schema["list_name_column"]:
            column_schema = table_schema["dict_column"][name_column]
            if column_schema["type_data_level"] == "unique":
                pass

            if column_schema["type_data_level"] == "categorical":
                list_data_frame_target.append(OnehotToCategorical.run(column_schema, data_frame_source))
            elif column_schema["type_data_level"] == "interval":
                series = data_frame_source[name_column]
                resolution = table_schema["dict_column"][name_column]["resolution"]
                list_data_frame_target.append(((series * (1 / resolution)).round().astype(int) * resolution).to_frame())

        return pandas.concat(list_data_frame_target, axis=1)

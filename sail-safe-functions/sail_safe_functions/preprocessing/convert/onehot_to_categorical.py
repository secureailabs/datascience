import numpy
import pandas


class OnehotToCategorical:
    def run(column_schema: dict, data_frame_source: pandas.DataFrame) -> pandas.DataFrame:
        name_column = column_schema["name_column"]
        type_missing_policy = column_schema["type_missing_policy"]
        if type_missing_policy not in ["propagate_add_column", "raise_exception"]:
            raise ValueError(type_missing_policy)

        list_name_column_selection = []
        for value in column_schema["list_value"]:
            list_name_column_selection.append(name_column + "_" + value)
        if type_missing_policy == "propagate_add_column":
            list_name_column_selection.append(name_column + "_nan")
        data_frame_selection = data_frame_source[list_name_column_selection]
        series = data_frame_selection.idxmax(axis=1)  # select the larges column name as value name
        series = series.str.slice(start=len(name_column) + 1)  # take away the prefixes
        series = series.replace("nan", numpy.nan)
        series.name = name_column
        return series.to_frame()

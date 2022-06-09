import numpy
import pandas


class ConvertCategoricalToOnehotFloat64:
    def run(column_schema: dict, data_frame_source: pandas.DataFrame) -> pandas.DataFrame:
        name_column = column_schema["name_column"]
        type_missing_policy = column_schema["type_missing_policy"]
        if type_missing_policy not in ["propagate_add_column", "raise_exception"]:
            raise ValueError(type_missing_policy)

        if type_missing_policy == "propagate_add_column":
            dummy_na = True
        else:
            dummy_na = False

        if type_missing_policy == "raise_exception":
            if 0 < data_frame_source[name_column].isna().sum():
                raise ValueError(f"Column {name_column} contains expeption while not should be present")

        data_frame_target = pandas.get_dummies(
            data_frame_source[name_column],
            prefix=name_column,
            prefix_sep="_",
            dummy_na=dummy_na,
            columns=column_schema["list_value"],
            sparse=False,
            drop_first=False,
            dtype=numpy.float64,
        )
        return data_frame_target


class ConvertOnehotFloat64ToCategorical:
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


class ConvertTabularToFloat64:
    def run(table_schema: dict, data_frame_source: pandas.DataFrame) -> pandas.DataFrame:

        list_data_frame_target = []
        for name_column in data_frame_source.columns:
            column_schema = table_schema["dict_column"][name_column]

            if column_schema["type_data_level"] == "unique":
                pass
            elif column_schema["type_data_level"] == "categorical":
                list_data_frame_target.append(ConvertCategoricalToOnehotFloat64.run(column_schema, data_frame_source))
            elif column_schema["type_data_level"] == "interval":
                list_data_frame_target.append(data_frame_source[name_column].astype(numpy.float64).to_frame())

        return pandas.concat(list_data_frame_target, axis=1)


class ConvertFloat64ToTabular:
    def run(table_schema: dict, data_frame_source: pandas.DataFrame) -> pandas.DataFrame:

        list_data_frame_target = []
        for name_column in table_schema["list_name_column"]:
            column_schema = table_schema["dict_column"][name_column]
            if column_schema["type_data_level"] == "unique":
                pass

            if column_schema["type_data_level"] == "categorical":
                list_data_frame_target.append(ConvertOnehotFloat64ToCategorical.run(column_schema, data_frame_source))
            elif column_schema["type_data_level"] == "interval":
                series = data_frame_source[name_column]
                resolution = table_schema["dict_column"][name_column]["resolution"]
                list_data_frame_target.append(((series * (1 / resolution)).round().astype(int) * resolution).to_frame())

        return pandas.concat(list_data_frame_target, axis=1)

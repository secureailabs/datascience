import numpy
import pandas


class CategoricalToOnehot:
    def run(column_schema: dict, data_frame_source: pandas.DataFrame) -> pandas.DataFrame:
        """
        Categorical featurization function

            :param column_schema: image.png
            :type column_schema: dictionary conating column schema
            :param data_frame_source: pandas dataframe conating source
            :type data_frame_source: pandas.DataFrame
            :return: featurized encoding on categorical feature
            :rtype: pandas.DataFrame
        """
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

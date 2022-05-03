import pandas as pd
from pandas.api.types import is_string_dtype
from sklearn.impute import SimpleImputer


class ImputeUnivariate:
    """
    Imputes one or more columns with a univariate strategy
    """

    def Run(data_frame: pd.DataFrame, list_name_column: list, strategy: str) -> pd.DataFrame:
        """Imputes one or more columns with a univariate strategy

        :param data_frame: Input dataframe
        :type data_frame: pd.DataFrame
        :param list_name_column: a list of column names to impute, set to None to do all columns
        :type list_name_column: list[str]
        :param strategy: strategy, must be either `mean`, `median` or `most_frequent`, on non-numerical data only must frequent is valid
        :type strategy: str
        :return: Output dataframe
        :rtype: pd.DataFrame
        """

        if strategy not in {"mean", "median", "most_frequent"}:
            raise ValueError("parameter `strategy` must be either mean, median or most_frequent")
        imputer = SimpleImputer(strategy=strategy)

        data_frame = data_frame.copy()
        if list_name_column is None:
            list_name_column = list(data_frame.columns)

        for name_column in list_name_column:

            if is_string_dtype(data_frame[name_column]) and strategy != "most_frequent":
                raise ValueError(
                    "`mean`, `median` strategies cannot not operate on column with name "
                    + name_column
                    + " which is of string type"
                )
            data_frame[name_column] = imputer.fit_transform(data_frame[[name_column]])

        return data_frame

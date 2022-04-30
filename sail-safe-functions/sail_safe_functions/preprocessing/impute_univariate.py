from statistics import median

import pandas as pd
from nbformat import read
from sklearn.impute import SimpleImputer


class ImputeUnivariate:
    """
    Drop rows or columns with missing data
    """

    def Run(data_frame: pd.DataFrame, strategy: str) -> pd.DataFrame:
        """ImputeUnivariate

        :param data_frame: Input dataframe
        :type data_frame: pd.DataFrame
        :param mode: strategy, must be either `mean`, `median` or `most_frequent`, on non-numerical data only must frequent is valid
        :type mode: str
        :return: Output dataframe
        :rtype: pd.DataFrame
        """

        if strategy not in {"mean", "median", "most_frequent"}:
            raise ValueError("strategy, must be either mean, median or most_frequent")
        imputer = SimpleImputer(strategy=strategy)
        return imputer.fit_transform(data_frame)


# imputer = SimpleImputer(strategy="mean", missing_values=np.nan)
# imputer = imputer.fit(df[["B"]])
# df["B"] = imputer.transform(df[["B"]])
# df

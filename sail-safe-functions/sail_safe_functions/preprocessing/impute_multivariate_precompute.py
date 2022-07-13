from typing import List

import pandas as pd
from pandas.api.types import is_numeric_dtype, is_string_dtype
from sklearn.experimental import enable_iterative_imputer  # NOTE side effect import!!!
from sklearn.impute import IterativeImputer, SimpleImputer


class ImputeMultivariatePrecompute:
    """
    Imputes one or more columns with a multivariate strategy
    uses https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html#sklearn.impute.IterativeImputer
    check https://towardsdatascience.com/iterative-imputation-with-scikit-learn-8f3eb22b1a38
    This only works wel on numerical columns!
    There is a trick we can do for string data as well using one-hot ecoding
    https://stackoverflow.com/questions/71622209/valueerror-could-not-convert-string-to-float-is-iterativeimputer-in-sklearn-onl
    but it is tricky to implement and might be out of scope
    """

    def run(
        data_frame: pd.DataFrame,
        list_name_column: List[str],
        imputation_order: str,
        max_iter: int = 10,
    ) -> pd.DataFrame:
        """Imputes one or more columns with a multivariate strategy

        :param data_frame: Input dataframe
        :type data_frame: pd.DataFrame
        :param list_name_column: a list of column names to impute, set to None to do all columns
        :type list_name_column: list[str]
        :param imputation_order: imputation_order, must be {`ascending`, `descending`}
            `ascending` From features with fewest missing values to most.
            `descending`: From features with most missing values to fewest.
        :type imputation_order: str
        :param max_iter: (default=10) maximum number of imputation rounds to perform before returning the imputations computed during the final round.
            The stopping criterion is met once max(abs(X_t - X_{t-1}))/max(abs(X[known_vals])) < tol, where X_t is X at iteration t.
        :type max_iter: int
        :return: Output dataframe
        :rtype: pd.DataFrame
        """

        # if strategy not in {"mean", "median", "most_frequent"}:
        #     raise ValueError("parameter `strategy` must be either mean, median or most_frequent")
        if imputation_order not in {"ascending", "descending"}:
            raise ValueError("parameter `imputation_order` must be either in {`ascending`, `descending`}")
        numerical_imputer = IterativeImputer(imputation_order=imputation_order, max_iter=max_iter)
        string_imputer = SimpleImputer(strategy="most_frequent")

        # Gather columns for imputation
        data_frame = data_frame.copy()
        if list_name_column is None:
            list_name_column_selected = list(data_frame.columns)
        else:
            list_name_column_selected = list_name_column

        # Gather numerical columns
        list_name_column_numeric = []
        for name_column in list(data_frame.columns):
            if is_numeric_dtype(data_frame[name_column]):
                list_name_column_numeric.append(name_column)

        # Impute numerical columns
        array_numeric_imputed = numerical_imputer.fit_transform(data_frame[list_name_column_numeric])
        data_frame_numeric_imputed = pd.DataFrame(array_numeric_imputed, columns=list_name_column_numeric)

        # Insert numerical columns
        for name_column in list_name_column_selected:
            if is_numeric_dtype(data_frame[name_column]):
                data_frame[name_column] = data_frame_numeric_imputed[name_column]
            elif is_string_dtype(data_frame[name_column]):
                data_frame[name_column] = string_imputer.fit_transform(data_frame[[name_column]])
        return data_frame

from typing import List

from pandas import DataFrame as DataFramePandas
from pandas.api.types import is_numeric_dtype, is_string_dtype
from sail_safe_functions_orchestrator.data_frame import DataFrame
from sail_safe_functions_orchestrator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions_orchestrator.series import Series
from sail_safe_functions_orchestrator.service_reference import ServiceReference
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
        reference_data_frame_source: ReferenceDataFrame,
        list_series_name_impute: List[str],
        imputation_order: str,
        max_iter: int = 10,
    ) -> ReferenceDataFrame:
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
        data_frame_source = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_source)
        if list_series_name_impute is None:
            list_series_name_impute = data_frame_source.list_series_name

        # Gather numerical columns
        list_series_name_numeric = []
        for series_name in list(data_frame_source.list_series_name):
            if is_numeric_dtype(data_frame_source[series_name]):
                list_series_name_numeric.append(series_name)

        # Impute numerical columns
        array_numeric_imputed = numerical_imputer.fit_transform(
            data_frame_source.select_series(list_series_name_numeric)
        )
        data_frame_numeric_imputed = DataFramePandas(array_numeric_imputed, columns=list_series_name_numeric)

        list_series = []
        # Insert numerical columns
        for series_name in data_frame_source.list_series_name:

            if series_name in list_series_name_impute:
                if series_name in list_series_name_numeric:
                    series_list = data_frame_numeric_imputed[series_name].tolist()

                elif is_string_dtype(data_frame_source[series_name]):
                    series_list = string_imputer.fit_transform(data_frame_source.select_series([series_name]))[
                        :, 0
                    ].tolist()
                series = Series(
                    data_frame_source.dataset_id,
                    data_frame_source[series_name].data_model_series,
                    series_list,
                )
                series.index = data_frame_source[series_name].index  # reattach index that sklearn removed
                list_series.append(series)
            else:
                list_series.append(data_frame_source[series_name])

        data_frame_target = DataFrame(data_frame_source.dataset_id, data_frame_source.data_frame_name, list_series)
        reference_data_frame_target = ServiceReference.get_instance().data_frame_to_reference(data_frame_target)
        return reference_data_frame_target

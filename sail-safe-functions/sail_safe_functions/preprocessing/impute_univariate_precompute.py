from typing import List

import pandas as pd
from pandas.api.types import is_string_dtype
from sail_safe_functions.safe_function_base import SafeFunctionBase
from sail_safe_functions_orchestrator.data_frame import DataFrame
from sail_safe_functions_orchestrator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions_orchestrator.series import Series
from sail_safe_functions_orchestrator.service_reference import ServiceReference
from sklearn.impute import SimpleImputer


class ImputeUnivariatePrecompute(SafeFunctionBase):
    """
    Imputes one or more columns with a univariate strategy
    """

    def run(
        reference_data_frame_source: ReferenceDataFrame, list_series_name_impute: List[str], strategy: str
    ) -> ReferenceDataFrame:
        """Imputes one or more columns with a univariate strategy

        :param data_frame: Input dataframe
        :type data_frame: pd.DataFrame
        :param list_series_name_impute: a list of series names to impute, set to None to do all columns
        :type list_series_name_impute: list[str]
        :param strategy: strategy, must be either `mean`, `median` or `most_frequent`, on non-numerical data only must frequent is valid
        :type strategy: str
        :return: Output dataframe
        :rtype: pd.DataFrame
        """

        if strategy not in {"mean", "median", "most_frequent"}:
            raise ValueError("parameter `strategy` must be either mean, median or most_frequent")
        imputer = SimpleImputer(strategy=strategy)

        data_frame_source = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame_source)
        if list_series_name_impute is None:
            list_series_name_impute = data_frame_source.list_series_name
        list_series = []
        for series_name in data_frame_source.list_series_name:
            if series_name in list_series_name_impute:
                if is_string_dtype(data_frame_source[series_name]) and strategy != "most_frequent":
                    raise ValueError(
                        f"`mean`, `median` strategies cannot not operate on series with series_name {series_name} which is of string type"
                    )

                series_list = imputer.fit_transform(data_frame_source.select_series([series_name]))[:, 0].tolist()
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

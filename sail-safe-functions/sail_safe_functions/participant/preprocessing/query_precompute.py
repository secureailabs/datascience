from typing import List

from sail_safe_functions.aggregator.data_frame import DataFrame
from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase


class QueryPrecompute(SafeFunctionBase):
    """
    Query the columns of a DataFrame with a boolean expression.
    """

    @staticmethod
    def run(
        reference_data_frame: ReferenceDataFrame,
        query_expresion: str,
        parser: str,
        local_dict: dict,
        global_dict: dict,
    ) -> ReferenceDataFrame:
        """
        Query the columns of a DataFrame with a boolean expression.

        :param data_frame: The target DataFrame
        :type data_frame: pandas.DataFrame
        :param query_expresion: The query string to evaluate
        :type query_expresion: str
        :param parser: The parser to use to construct the syntax tree from the expression. The default of 'pandas' parses code slightly different than standard Python. Alternatively, you can parse an expression using the 'python' parser to retain strict Python semantics. See the https://pandas.pydata.org/docs/user_guide/enhancingperf.html#enhancingperf-eval documentation for more details.
        :type parser: str
        :param local_dict: A dictionary of local variables, taken from locals() by default.
        :type local_dict: dict
        :param global_dict: A dictionary of global variables, taken from globals() by default.
        :type global_dict: dict
        :return: DataFrame resulting from the provided query expression.
        :rtype: List
        """
        data_frame_source = ServiceReference.get_instance().reference_to_data_frame(reference_data_frame)
        data_frame_pandas = data_frame_source.query(  # TODO overload this one
            query_expresion,
            parser=parser,
            local_dict=local_dict,
            global_dict=global_dict,
        )
        data_frame_target = DataFrame.from_pandas(
            data_frame_source.dataset_id,
            data_frame_source.data_frame_name,
            data_frame_source.data_model_data_frame,
            data_frame_pandas,
        )

        return ServiceReference.get_instance().data_frame_to_reference(data_frame_target)

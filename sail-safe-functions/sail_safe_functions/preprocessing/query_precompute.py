from typing import Any, List

import pandas


class QueryPrecompute:
    """
    Query the columns of a DataFrame with a boolean expression.
    """

    def run(
        data_frame: pandas.DataFrame,
        query_expresion: str,
        parser: str,
        local_dict: dict,
        global_dict: dict,
    ) -> List:
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
        return data_frame.query(
            query_expresion,
            parser=parser,
            local_dict=local_dict,
            global_dict=global_dict,
        )

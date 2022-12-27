import ast
import io
import os
import sys
from typing import Any, List

import numpy as np
import pandas as pd
from pandas.core.computation.expr import Expr, Scope
from sail_safe_functions.aggregator.data_frame_federated import DataFrameFederated
from sail_safe_functions.aggregator.tools_common import check_instance
from sail_safe_functions.aggregator.tools_specific.parser import unparse
from sail_safe_functions.participant.preprocessing.query_precompute import QueryPrecompute


def query(
    data_frame_source: DataFrameFederated,
    query_expression: str,
    parser: str = "pandas",
    local_dict: dict = None,
    global_dict: dict = None,
) -> DataFrameFederated:
    """
    Federated equivalent of (pd.DataFrame.query)
    """
    return Query.run(data_frame_source, query_expression, parser, local_dict, global_dict)


class Query:
    """
    Federated equivalent of (pd.DataFrame.query)
    """

    @staticmethod
    def run(
        data_frame_source: DataFrameFederated,
        query_expression: str,
        parser: str,
        local_dict: dict,
        global_dict: dict,
    ) -> DataFrameFederated:
        """
        Perform federated query (pandas.DataFrame.query) function

        :param data_frame_source: The target DataFrame
        :type data_frame_source: DataFrameFederated
        :param query_expression: The query string to evaluate. You can refer to variables in the environment by prefixing them with an ‘@’ character like @a + b. You can refer to column names that are not valid Python variable names by surrounding them in backticks. Thus, column names containing spaces or punctuations (besides underscores) or starting with digits must be surrounded by backticks. (For example, a column named “Area (cm^2)” would be referenced as `Area (cm^2)`). Column names which are Python keywords (like “list”, “for”, “import”, etc) cannot be used. For example, if one of your columns is called a a and you want to sum it with b, your query should be `a a` + b.
        :type query_expression: str
        :param parser: The parser to use to construct the syntax tree from the expression. The default of 'pandas' parses code slightly different than standard Python. Alternatively, you can parse an expression using the 'python' parser to retain strict Python semantics. See the https://pandas.pydata.org/docs/user_guide/enhancingperf.html#enhancingperf-eval documentation for more details.
        :type parser: str
        :param local_dict: A dictionary of local variables, taken from locals() by default.
        :type local_dict: dict
        :param global_dict: A dictionary of global variables, taken from globals() by default.
        :type global_dict: dict
        :return: Federated DataFrame resulting from the provided query expression.
        :rtype: DataFrameFederated
        """
        check_instance(data_frame_source, DataFrameFederated)
        check_instance(query_expression, str)
        check_instance(parser, str)
        check_instance(local_dict, (dict, type(None)))
        check_instance(global_dict, (dict, type(None)))

        caller_frame = sys._getframe(2)
        local_dict = local_dict if local_dict else caller_frame.f_locals
        global_dict = global_dict if global_dict else caller_frame.f_globals

        validated_query = Query.validate_query(
            query_expression,
            parser,
        )
        validated_local_dict, validated_global_dict = Query._validate_envs(local_dict, global_dict)

        list_reference = data_frame_source.map_function(
            QueryPrecompute,
            validated_query,
            parser,
            validated_local_dict,
            validated_global_dict,
        )

        return DataFrameFederated(list_reference, data_frame_source.data_model_data_frame)

    # Target dataframe will be allowed even if pd.DataFrame is not included here
    _allowed_var_types = frozenset(
        [
            str,
            int,
            float,
            bool,
            type(None),
            np.int_,
            np.int8,
            np.int16,
            np.int32,
            np.int64,
            np.float_,
            np.float16,
            np.float32,
            np.float64,
        ]
    )

    _allowed_builtins = {
        "False": False,
        "True": True,
        "None": None,
    }

    # See https://docs.python.org/3/library/ast.html#abstract-grammar
    # We can add more functionalities by adding nodes
    _allowed_node_types = frozenset(
        [
            # Modules needed for parsing
            ast.Module,
            ast.Expr,
            # Allowed subclasses of ast.expr
            ast.BoolOp,
            ast.BinOp,
            ast.UnaryOp,
            ast.Compare,
            ast.Constant,
            ast.Name,
            # Allowed subclasses of ast.expr_context
            ast.Load,
            # Boolean operators
            ast.boolop,
            # Operators
            ast.operator,
            # Allowed sublclasses of ast.unaryop
            ast.Not,
            # Comparison operators
            ast.cmpop,
        ]
    )

    @staticmethod
    def validate_query(
        query_string: str,
        parser: str,
        force_parse: bool = True,
    ):
        """
        Validates query for DataFrameFederatedLocal.query function.

        Parameters
        ----------
        query_string : str
            String to validate.
        parser : str
            Same as pd.DataFrame.query parser parameter.
        force_parse : bool = True
            str -> AST -> str parsing can make output code less optimize than the input (https://docs.python.org/3/library/ast.html#ast.unparse). However, for security purposes it's better to return a parsed string rather than just a validated string.
        Returns
        -------
        str
            The validated string.
        """
        check_instance(query_string, str)
        check_instance(parser, str)
        check_instance(force_parse, bool)

        # Only an empty string query '' is evaluated here, it's just string manipulation to support special Pandas syntax (e.g. backticks (``))
        pandas_cleaned_string = Expr("''", engine="numexpr", parser=parser, env=Scope(0))._visitor.preparser(
            query_string
        )

        # AST as generated and cleaned in Pandas but with Python builtin module
        query_ast = ast.fix_missing_locations(ast.parse(pandas_cleaned_string))

        # Now that we have the exact same AST as Pandas will have while evaluating our query,
        # we inspect it to make sure it doesn't contain anything we don't want
        # (More rigorous implementation with NodeVisitor subclass could potentially be usefull for implementing DP)
        expended_allowed_node_types = AstUtils.get_expended_allowed_node_types(Query._allowed_node_types)
        for node in ast.walk(query_ast):
            # Only allow allowed node types
            if type(node) not in expended_allowed_node_types:
                # Error message is vague on purpose for security reasons
                raise ValueError("Invalid query")

        if force_parse:
            unparse_buffer = io.StringIO()
            unparse.Unparser(query_ast, unparse_buffer)
            validated_query = unparse_buffer.getvalue()
        else:
            validated_query = pandas_cleaned_string

        return validated_query

    def _validate_envs(local_dict, global_dict) -> frozenset([dict, dict]):
        """
        Removes all unwanted variables of scope

        Parameters
        ----------
        local_dict : dict
            Original local_dict that will be filtered then given to pd.query
        global_dict : dict
            Original global_dict that will be filtered then given to pd.query

        Returns
        -------
        (local_dict : dict, global_dict : dict)
            local_dict :
                Safe local dict
            global_dict :
                Safe global dict
        """
        safe_local_dict = {key: value for key, value in local_dict.items() if type(value) in Query._allowed_var_types}
        safe_global_dict = {key: value for key, value in global_dict.items() if type(value) in Query._allowed_var_types}
        # Without this, eval would be allowed to use all of builtins module (see https://docs.python.org/3/library/functions.html#eval)
        safe_local_dict["__builtins__"] = Query._allowed_builtins
        safe_global_dict["__builtins__"] = Query._allowed_builtins

        return safe_local_dict, safe_global_dict


class AstUtils:
    """
    AST utils adapted from https://github.com/pandas-dev/pandas/blob/a6aaeb6baf679fe133e968e0f65199fc56d177b2/pandas/core/computation/expr.py#L180
    """

    _all_nodes = frozenset(
        node
        for node in (getattr(ast, name) for name in dir(ast))
        if isinstance(node, type) and issubclass(node, ast.AST)
    )

    def _filter_nodes(superclass):
        """
        Filter out AST nodes that are subclasses of ``superclass``.
        """
        node_names = [node for node in AstUtils._all_nodes if issubclass(node, superclass)]
        return node_names

    # We have to do it this way instead of using issubclass directly on query nodes because
    # an attacker could make a custom child class of Ast.<allowed_node> which we don't want to allow
    def get_expended_allowed_node_types(allowed_node_types: frozenset) -> frozenset:
        expended_allowed_node_types = []

        for node_type in Query._allowed_node_types:
            expended_allowed_node_types += AstUtils._filter_nodes(node_type)

        return frozenset(expended_allowed_node_types)

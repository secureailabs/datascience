from typing import List
from sail_safe_functions.safe_function_base import SafeFunctionBase

class ListCreate(SafeFunctionBase):
    """
    Creates an empty list for aggregation
    """

    def run() -> List:
        #TODO dont think we still use this
        """Creates an empty list for aggregation

        :return: The created list
        :rtype: List
        """
        return []

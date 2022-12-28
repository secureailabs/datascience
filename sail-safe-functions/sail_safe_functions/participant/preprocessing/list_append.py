from typing import Any, List

from sail_safe_functions.safe_function_base import SafeFunctionBase


class ListAppend:
    """
    Appends an element to a list
    """

    def run(list: List, element: Any) -> List:
        # TODO dont think we still use this
        """Appends an element to a list for aggregation

        :param list: The list to append an element to
        :type list: List
        :param element: The element to append
        :type element: Any
        :return: The list with the element appended
        :rtype: List
        """
        list.append(element)
        return list

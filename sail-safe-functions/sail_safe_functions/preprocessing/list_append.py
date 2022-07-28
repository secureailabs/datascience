from typing import Any, List


class ListAppend:
    """
    Appends an element to a list
    """

    def Run(list: List, element: Any) -> List:
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

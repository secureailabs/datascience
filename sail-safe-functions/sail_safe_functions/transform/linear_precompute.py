from array import array
from typing import List

import numpy
import pandas


class LinearPrecompute:
    """
    Do a linear transform
    """

    def run(
        data_frame_source: pandas.DataFrame,
        array_add: numpy.ndarray,
        array_dot_product: numpy.ndarray,
        list_name_feature_source: List[str],
        list_name_feature_target: List[str],
    ):
        # TODO get rid of the add matrix

        array_source = data_frame_source[list_name_feature_source].to_numpy().astype(numpy.float64)
        # add the addition array per column
        array_add = array_source + numpy.outer(numpy.ones(array_source.shape[0]), array_add)
        # do the dot transform
        array_target = numpy.dot(array_add, array_dot_product)
        data_frame_target = data_frame_source.copy()
        for i, name_feature in enumerate(list_name_feature_target):
            data_frame_target[name_feature] = pandas.Series(data=array_target[:, i], name=name_feature)
        return data_frame_target

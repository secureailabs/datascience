from typing import Optional, Type

import numpy as np
from zero import SecretObject


# to do: need to check how to annotate, pass a star argument
def array(
    obj: list,
    dtype: Optional[str] = None,
    copy: bool = True,
    order: str = "K",
    subok: bool = False,
    ndmin: int = 0,
    like: Optional[list] = None,
) -> Type[SecretObject]:
    """
    create a numpy array from list

    :param obj: list to be processed
    :type obj: list
    :param dtype: data types, defaults to None
    :type dtype: str, optional
    :param copy: when the obj is numpy array, whether to create a new instance, defaults to True
    :type copy: bool, optional
    :param order: memory layout of the array, defaults to "K"
    :type order: str, optional
    :param subok: if it is a sub class array, defaults to False
    :type subok: bool, optional
    :param ndmin: minimum number of dimensions, defaults to 0
    :type ndmin: int, optional
    :param like: array reference, defaults to None
    :type like: np.ndarray, optional
    :return: numpy array
    :rtype: np.ndarray
    """
    ans = np.array(obj)
    return SecretObject(ans)


def random_normal(
    loc: float = 0.0,
    scale: float = 1.0,
    size: Optional[int] = None,
    seed: int = 42,
) -> Type[SecretObject]:
    np.random.seed(seed)
    res = np.random.normal(loc, scale, size)
    return SecretObject(res)


# to do
class RemoteNumpyArray:
    def __init__(
        self,
    ):
        pass

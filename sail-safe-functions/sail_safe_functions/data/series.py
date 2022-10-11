from typing import Callable, Hashable, List, Literal, Optional, Type, Union

import pandas as pd
from pandas._libs.lib import no_default
from sail_safe_functions.data.typing import (
    ArrayLike,
    Axis,
    Frequency,
    IndexLabel,
    Level,
    Scalar,
    TimedeltaConvertibleTypes,
    TimestampConvertibleTypes,
    copy_doc,
)
from zero import ProxyObject, SecretObject


class SeriesRemote:
    def __init__(
        self,
        d=None,
        ind=None,
        typ=None,
        na=None,
    ):
        """
        constructor, accept same value as pd.Series or a raw pd.Seris instance object

        :param d: input data, defaults to None
        :type d: dict, arraylike, optional
        :param ind: index, defaults to None
        :type ind: str, list of str, optional
        :param typ: data type, defaults to None
        :type typ: str, optional
        :param na: representation of missing value, defaults to None
        :type na: no_default, optional
        """
        if d is None or isinstance(d, pd.Series):
            self.series = d
        else:
            self.series = pd.Series(data=d, index=ind, dtype=typ, name=na)
        if self.series is not None:
            self.index = self.series.index
            self.values = SecretObject(self.series.values)
            self.dtypes = self.series.dtypes
            self.shape = self.series.shape
            self.nbytes = self.series.nbytes
            self.ndim = self.series.ndim
            self.size = self.series.size
            self.hasnans = self.series.hasnans
            self.empty = self.series.empty
            self.name = self.series.name

    @property
    def at(self):
        return ProxyObject(self.series.at)

    @property
    def iat(self):
        return ProxyObject(self.series.iat)

    @property
    def loc(self):
        return ProxyObject(self.series.loc)

    @property
    def iloc(self):
        return ProxyObject(self.series.iloc)

    def ravel(
        self,
        order: str = "C",
    ) -> Type[ProxyObject]:
        ans = self.series.ravel(order)
        return ProxyObject(ans)

    @copy_doc(pd.Series.repeat)
    def repeat(
        self,
        repeats: Union[int, List[int]],
        axis=None,
    ) -> Type[ProxyObject]:
        ans = self.series.repeat(repeats, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.reset_index)
    def reset_index(
        self,
        level: Optional[Union[int, str, tuple, list]] = None,
        drop: bool = False,
        name: Optional[str] = no_default,
        inplace: bool = False,
    ) -> Type[ProxyObject]:
        ans = self.series.reset_index(level, drop, name, inplace)
        return ProxyObject(ans)

    # def items(self) -> 'Iterable[tuple[Hashable, Any]]':
    #     ans = self.series.items()

    # def iteritems(self) -> 'Iterable[tuple[Hashable, Any]]':
    #     ans = self.series.iteritems()

    @copy_doc(pd.Series.keys)
    def keys(self) -> ArrayLike:
        ans = self.series.keys()
        return ans

    @copy_doc(pd.Series.to_dict)
    def to_dict(
        self,
        into=dict,
    ) -> dict:
        ans = self.series.to_dict(into)
        return ProxyObject(ans)

    def to_series(
        self,
        name: "Hashable" = no_default,
    ) -> Type[ProxyObject]:
        ans = self.series.to_series(name)
        return ProxyObject(ans)

    @copy_doc(pd.Series.to_numpy)
    def to_numpy(
        self,
        dtype: Optional[str] = None,
        copy: bool = False,
    ) -> Type[SecretObject]:
        ans = self.series.to_numpy(dtype=dtype, copy=copy)
        return SecretObject(ans)

    # ?
    @copy_doc(pd.Series.groupby)
    def groupby(
        self,
        by: IndexLabel = None,
        axis: Axis = 0,
        level: Optional[Level] = None,
        as_index: bool = True,
        sort: bool = True,
        group_keys: bool = True,
        squeeze: Optional[bool] = no_default,
        observed: bool = False,
        dropna: bool = True,
    ) -> Type[ProxyObject]:
        ans = self.series.groupby(by, axis, level, as_index, sort, group_keys, squeeze, observed, dropna)
        return ProxyObject(ans)

    @copy_doc(pd.Series.count)
    def count(
        self,
        level: Optional[Level] = None,
    ) -> Union[int, pd.Series]:
        ans = self.series.count(level)
        return ans

    # ?
    @copy_doc(pd.Series.mode)
    def mode(
        self,
        dropna: "bool" = True,
    ) -> pd.Series:
        ans = self.series.mode(dropna)
        return ans

    @copy_doc(pd.Series.unique)
    def unique(
        self,
    ) -> "ArrayLike":
        ans = self.series.unique()
        return ans

    @copy_doc(pd.Series.drop_duplicates)
    def drop_duplicates(
        self,
        keep: str = "first",
        inplace: bool = False,
    ) -> Type[ProxyObject]:
        ans = self.series.drop_duplicates(keep, inplace)
        return ProxyObject(ans)

    @copy_doc(pd.Series.duplicated)
    def duplicated(
        self,
        keep: str = "first",
    ) -> Type[ProxyObject]:
        ans = self.series.duplicated(keep)
        return ProxyObject(ans)

    @copy_doc(pd.Series.idxmin)
    def idxmin(
        self,
        axis: Axis = 0,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> IndexLabel:
        ans = self.series.idxmin(axis, skipna, *args, **kwargs)
        return ans

    @copy_doc(pd.Series.idxmax)
    def idxmax(
        self,
        axis: Axis = 0,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> IndexLabel:
        ans = self.series.idxmax(axis, skipna, *args, **kwargs)
        return ans

    @copy_doc(pd.Series.round)
    def round(
        self,
        decimals=0,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.round(decimals, *args, **kwargs)
        return ProxyObject[ans]

    @copy_doc(pd.Series.quantile)
    def quantile(
        self,
        q: float = 0.5,
        interpolation: str = "linear",
    ) -> Union[float, pd.Series]:
        ans = self.series.quantile(q, interpolation)
        return ans

    @copy_doc(pd.Series.corr)
    def corr(
        self,
        other: pd.Series,
        method: str = "pearson",
        min_periods: Optional[int] = None,
    ) -> "float":
        ans = self.series.corr(other, method, min_periods)
        return ans

    @copy_doc(pd.Series.cov)
    def cov(
        self,
        other: pd.Series,
        min_periods: "int | None" = None,
        ddof: "int | None" = 1,
    ) -> "float":
        ans = self.series.cov(other, min_periods, ddof)
        return ans

    @copy_doc(pd.Series.diff)
    def diff(
        self,
        periods: "int" = 1,
    ) -> Type[ProxyObject]:
        ans = self.series.diff(periods)
        return ProxyObject(ans)

    @copy_doc(pd.Series.autocorr)
    def autocorr(
        self,
        lag: int = 1,
    ) -> "float":
        ans = self.series.autocorr(lag)
        return ans

    @copy_doc(pd.Series.dot)
    def dot(
        self,
        other: ArrayLike,
    ) -> Type[ProxyObject]:
        ans = self.series.dot(other)
        return ProxyObject(ans)

    # ?
    @copy_doc(pd.Series.searchsorted)
    def searchsorted(
        self,
        value: Union[ArrayLike, Scalar],
        side: Literal["left", "right"] = "left",
        sorter: Optional[ArrayLike] = None,
    ) -> Union[int, List[int]]:
        ans = self.series.searchsorted(value, side, sorter)
        return ans

    @copy_doc(pd.Series.compare)
    def compare(
        self,
        other: pd.Series,
        align_axis: "Axis" = 1,
        keep_shape: "bool" = False,
        keep_equal: "bool" = False,
    ) -> Type[ProxyObject]:
        ans = self.series.compare(other, align_axis, keep_shape, keep_equal)
        return ProxyObject(ans)

    @copy_doc(pd.Series.combine)
    def combine(
        self,
        other: Union[Scalar, pd.Series],
        func: Callable,
        fill_value: Optional[Scalar] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.combine(other, func, fill_value)
        return ProxyObject(ans)

    @copy_doc(pd.Series.combine_first)
    def combine_first(
        self,
        other: pd.Series,
    ) -> Type[ProxyObject]:
        ans = self.series.combine_first(other)
        return ProxyObject(ans)

    @copy_doc(pd.Series.update)
    def update(
        self,
        other: pd.Series,
    ) -> "None":
        ans = self.series.update(other)

    @copy_doc(pd.Series.sort_values)
    def sort_values(
        self,
        axis: Axis = 0,
        ascending: Union[bool, int] = True,
        inplace: bool = False,
        kind: str = "quicksort",
        na_position: str = "last",
        ignore_index: bool = False,
        key: Optional[Callable] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.sort_values(axis, ascending, inplace, kind, na_position, ignore_index, key)
        return ProxyObject(ans)

    @copy_doc(pd.Series.sort_index)
    def sort_index(
        self,
        axis: Axis = 0,
        ascending: Union[bool, int] = True,
        inplace: bool = False,
        kind: str = "quicksort",
        na_position: str = "last",
        ignore_index: bool = False,
        key: Optional[Callable] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.sort_index(axis, ascending, inplace, kind, na_position, ignore_index, key)
        return ProxyObject(ans)

    @copy_doc(pd.Series.argsort)
    def argsort(
        self,
        axis: Axis = 0,
        kind: str = "quicksort",
        order: None = None,
    ) -> Type[ProxyObject]:
        ans = self.series.argsort(axis, kind, order)
        return ProxyObject(ans)

    @copy_doc(pd.Series.nlargest)
    def nlargest(
        self,
        n: int = 5,
        keep: str = "first",
    ) -> Type[ProxyObject]:
        ans = self.series.nlargest(n, keep)
        return ProxyObject(ans)

    @copy_doc(pd.Series.nsmallest)
    def nsmallest(
        self,
        n: "int" = 5,
        keep: "str" = "first",
    ) -> Type[ProxyObject]:
        ans = self.series.nsmallest(n, keep)
        return ProxyObject(ans)

    @copy_doc(pd.Series.swaplevel)
    def swaplevel(
        self,
        i: int = -2,
        j: int = -1,
        copy: bool = True,
    ) -> Type[ProxyObject]:
        ans = self.series.swaplevel(i, j, copy)
        return ProxyObject(ans)

    @copy_doc(pd.Series.reorder_levels)
    def reorder_levels(
        self,
        order: List[int],
    ) -> Type[ProxyObject]:
        ans = self.series.reorder_levels(order)
        return ProxyObject(ans)

    @copy_doc(pd.Series.explode)
    def explode(
        self,
        ignore_index: "bool" = False,
    ) -> Type[ProxyObject]:
        ans = self.series.explode(ignore_index)
        return ProxyObject(ans)

    @copy_doc(pd.Series.unstack)
    def unstack(
        self,
        level: int = -1,
        fill_value: Optional[Scalar] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.unstack(level, fill_value)
        return ProxyObject(ans)

    @copy_doc(pd.Series.map)
    def map(
        self,
        arg: Callable,
        na_action: Optional[str] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.map(arg, na_action)
        return ProxyObject(ans)

    @copy_doc(pd.Series.aggregate)
    def aggregate(
        self,
        func: Callable = None,
        axis: Axis = 0,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.aggregate(func, axis, *args, **kwargs)
        return ProxyObject(ans)

    @copy_doc(pd.Series.transform)
    def transform(
        self,
        func: Callable,
        axis: "Axis" = 0,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.transform(func, axis, *args, **kwargs)
        return ProxyObject(ans)

    @copy_doc(pd.Series.apply)
    def apply(
        self,
        func: Callable,
        convert_dtype: "bool" = True,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.apply(func, convert_dtype, *args, **kwargs)
        return ProxyObject(ans)

    @copy_doc(pd.Series.align)
    def align(
        self,
        other: Union[pd.DataFrame, pd.Series],
        join: str = "outer",
        axis: Union[Axis, None] = None,
        level: Union[Level, None] = None,
        copy: bool = True,
        fill_value=None,
        method: Union[str, None] = None,
        limit=None,
        fill_axis: Axis = 0,
        broadcast_axis: Union[Axis, None] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.align(other, join, axis, level, copy, fill_value, method, limit, fill_axis, broadcast_axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.rename)
    def rename(
        self,
        index: Union[Scalar, Hashable, dict, Callable] = None,
        *,
        axis: Optional[Axis] = None,
        copy: bool = True,
        inplace: bool = False,
        level: Optional[Level] = None,
        errors: str = "ignore",
    ) -> Type[ProxyObject]:
        ans = self.series.rename(index, axis, copy, inplace, level, errors)
        return ProxyObject(ans)

    @copy_doc(pd.Series.set_axis)
    def set_axis(
        self,
        labels: IndexLabel,
        axis: "Axis" = 0,
        inplace: "bool" = False,
    ) -> Type[ProxyObject]:
        ans = self.series.set_axis(labels, axis, inplace)
        return ProxyObject(ans)

    @copy_doc(pd.Series.reindex)
    def reindex(
        self,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.reindex(args, **kwargs)
        return ProxyObject(ans)

    @copy_doc(pd.Series.drop)
    def drop(
        self,
        labels: Optional[IndexLabel] = None,
        axis: Axis = 0,
        index: Optional[IndexLabel] = None,
        columns: Optional[IndexLabel] = None,
        level: Optional[Level] = None,
        inplace: bool = False,
        errors: str = "raise",
    ) -> Type[ProxyObject]:
        ans = self.series.drop(labels, axis, index, columns, level, inplace, errors)
        return ProxyObject(ans)

    @copy_doc(pd.Series.fillna)
    def fillna(
        self,
        value: Optional[Union[Scalar, ArrayLike]] = None,
        method: Optional[str] = None,
        axis: Axis = None,
        inplace: bool = False,
        limit: Optional[int] = None,
        downcast: Optional[dict] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.fillna(value, method, axis, inplace, limit, downcast)
        return ProxyObject(ans)

    @copy_doc(pd.Series.pop)
    def pop(
        self,
        item: "Hashable",
    ) -> Type[ProxyObject]:
        ans = self.series.pop(item)
        return ProxyObject(ans)

    @copy_doc(pd.Series.replace)
    def replace(
        self,
        to_replace: Optional[Union[Scalar, pd.Series]] = None,
        value: Optional[Union[Scalar, list, dict]] = no_default,
        inplace: Optional[bool] = False,
        limit: Optional[int] = None,
        regex: bool = False,
        method: Optional[str] = no_default,
    ) -> Type[ProxyObject]:
        ans = self.series.replace(to_replace, value, inplace, limit, regex, method)
        return ProxyObject(ans)

    @copy_doc(pd.Series.shift)
    def shift(
        self,
        periods: int = 1,
        freq: Optional[Frequency] = None,
        axis: Axis = 0,
        fill_value: Optional[Scalar] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.shift(periods, freq, axis, fill_value)
        return ProxyObject(ans)

    @copy_doc(pd.Series.memory_usage)
    def memory_usage(
        self,
        index: "bool" = True,
        deep: "bool" = False,
    ) -> "int":
        ans = self.series.memory_usage(index, deep)
        return ans

    @copy_doc(pd.Series.isin)
    def isin(
        self,
        values: Union[set, list],
    ) -> Type[ProxyObject]:
        ans = self.series.isin(values)
        return ProxyObject(ans)

    @copy_doc(pd.Series.between)
    def between(
        self,
        left: Union[Scalar, list],
        right: Union[Scalar, list],
        inclusive: str = "both",
    ) -> Type[ProxyObject]:
        ans = self.series.between(left, right, inclusive)
        return ProxyObject(ans)

    @copy_doc(pd.Series.isna)
    def isna(
        self,
    ) -> Type[ProxyObject]:
        ans = self.series.isna()
        return ProxyObject(ans)

    @copy_doc(pd.Series.isnull)
    def isnull(
        self,
    ) -> Type[ProxyObject]:
        ans = self.series.isnull()
        return ProxyObject(ans)

    @copy_doc(pd.Series.notna)
    def notna(
        self,
    ) -> Type[ProxyObject]:
        ans = self.series.notna()
        return ProxyObject(ans)

    @copy_doc(pd.Series.notnull)
    def notnull(
        self,
    ) -> Type[ProxyObject]:
        ans = self.series.notnull()
        return ProxyObject(ans)

    @copy_doc(pd.Series.dropna)
    def dropna(
        self,
        axis: Axis = 0,
        inplace: bool = False,
        how: Optional[str] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.dropna(axis, inplace, how)
        return ProxyObject(ans)

    @copy_doc(pd.Series.asfreq)
    def asfreq(
        self,
        freq: Frequency,
        method: Optional[str] = None,
        how: "str | None" = None,
        normalize: "bool" = False,
        fill_value: Scalar = None,
    ) -> Type[ProxyObject]:
        ans = self.series.asfreq(freq, method, how, normalize, fill_value)
        return ProxyObject(ans)

    # ? todo
    @copy_doc(pd.Series.resample)
    def resample(
        self,
        rule,
        axis=0,
        closed: "str | None" = None,
        label: "str | None" = None,
        convention: "str" = "start",
        kind: "str | None" = None,
        loffset=None,
        base: "int | None" = None,
        on=None,
        level=None,
        origin: "str | TimestampConvertibleTypes" = "start_day",
        offset: "TimedeltaConvertibleTypes | None" = None,
    ) -> "None":
        ans = self.series.resample(
            rule, axis, closed, label, convention, kind, loffset, base, on, level, origin, offset
        )
        return ProxyObject(ans)

    @copy_doc(pd.Series.to_timestamp)
    def to_timestamp(
        self,
        freq: Optional[Frequency] = None,
        how: str = "start",
        copy: bool = True,
    ) -> Type[ProxyObject]:
        ans = self.series.to_timestamp(freq, how, copy)
        return ProxyObject(ans)

    @copy_doc(pd.Series.to_period)
    def to_period(
        self,
        freq: Optional[Frequency] = None,
        copy: bool = True,
    ) -> Type[ProxyObject]:
        ans = self.series.to_period(freq, copy)
        return ProxyObject(ans)

    @copy_doc(pd.Series.ffill)
    def ffill(
        self,
        axis: "None | Axis" = None,
        inplace: "bool" = False,
        limit: "None | int" = None,
        downcast: Optional[dict] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.ffill(axis, inplace, limit, downcast)
        return ProxyObject(ans)

    @copy_doc(pd.Series.bfill)
    def bfill(
        self,
        axis: "None | Axis" = None,
        inplace: "bool" = False,
        limit: "None | int" = None,
        downcast: Optional[dict] = None,
    ) -> Type[ProxyObject]:
        ans = self.series.bfill(axis, inplace, limit, downcast)
        return ProxyObject(ans)

    @copy_doc(pd.Series.clip)
    def clip(
        self,
        lower: Optional[Union[float, ArrayLike]] = None,
        upper: Optional[Union[float, ArrayLike]] = None,
        axis: "Axis | None" = None,
        inplace: "bool" = False,
        *args,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.clip(lower, upper, axis, inplace, *args, **kwargs)
        return ProxyObject(ans)

    @copy_doc(pd.Series.interpolate)
    def interpolate(
        self,
        method: "str" = "linear",
        axis: "Axis" = 0,
        limit: "int | None" = None,
        inplace: "bool" = False,
        limit_direction: "str | None" = None,
        limit_area: "str | None" = None,
        downcast: "str | None" = None,
        **kwargs,
    ) -> Type[ProxyObject]:
        ans = self.series.interpolate(method, axis, limit, inplace, limit_direction, limit_area, downcast, **kwargs)
        return ProxyObject(ans)

    @copy_doc(pd.Series.where)
    def where(
        self,
        cond: Union[bool, ArrayLike, Callable],
        other: Union[ArrayLike, Callable] = no_default,
        inplace: bool = False,
        axis: Optional[int] = None,
        level: Optional[int] = None,
        errors: str = "raise",
        try_cast: Optional[bool] = no_default,
    ) -> Type[ProxyObject]:
        ans = self.series.where(cond, other, inplace, axis, level, errors, try_cast)
        return ProxyObject(ans)

    @copy_doc(pd.Series.mask)
    def mask(
        self,
        cond: Union[bool, ArrayLike, Callable],
        other: Union[ArrayLike, Callable] = no_default,
        inplace: bool = False,
        axis: Optional[int] = None,
        level: Optional[int] = None,
        errors: str = "raise",
        try_cast: Optional[bool] = no_default,
    ) -> Type[ProxyObject]:
        ans = self.series.mask(cond, other, inplace, axis, level, errors, try_cast)
        return ProxyObject(ans)

    @copy_doc(pd.Series.abs)
    def abs(
        self,
    ) -> Type[ProxyObject]:
        ans = self.series.abs()
        ans = SeriesRemote(d=ans)
        return ProxyObject(ans)

    @copy_doc(pd.Series.any)
    def any(
        self,
        axis: Axis = 0,
        bool_only: Optional[bool] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.any(axis, bool_only, skipna, level, **kwargs)
        return ans

    @copy_doc(pd.Series.all)
    def all(
        self,
        axis: Axis = 0,
        bool_only: Optional[bool] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.all(axis, bool_only, skipna, level, **kwargs)
        return ans

    @copy_doc(pd.Series.mad)
    def mad(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.mad(axis, skipna, level)
        return ans

    @copy_doc(pd.Series.sem)
    def sem(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        ddof: int = 1,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.sem(axis, skipna, level, ddof, numeric_only, **kwargs)
        return ans

    @copy_doc(pd.Series.var)
    def var(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        ddof: int = 1,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.var(axis, skipna, level, ddof, numeric_only, **kwargs)
        return ans

    @copy_doc(pd.Series.std)
    def std(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        ddof: int = 1,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.std(axis, skipna, level, ddof, numeric_only, **kwargs)
        return ans

    @copy_doc(pd.Series.cummin)
    def cummin(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.cummin(axis, skipna, *args, **kwargs)
        return ans

    @copy_doc(pd.Series.cummax)
    def cummax(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.cummax(axis, skipna, *args, **kwargs)
        return ans

    @copy_doc(pd.Series.cumsum)
    def cumsum(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.cumsum(axis, skipna, *args, **kwargs)
        return ans

    @copy_doc(pd.Series.cumprod)
    def cumprod(
        self,
        axis: Optional[Axis] = None,
        skipna: bool = True,
        *args,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.cumprod(axis, skipna, *args, **kwargs)
        return ans

    @copy_doc(pd.Series.sum)
    def sum(
        self,
        axis: Axis = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        min_count: int = 0,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.sum(axis, skipna, level, numeric_only, min_count, **kwargs)
        return ans

    @copy_doc(pd.Series.prod)
    def prod(
        self,
        axis: Axis = None,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        min_count: int = 0,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.prod(axis, skipna, level, numeric_only, min_count, **kwargs)
        return ans

    @copy_doc(pd.Series.mean)
    def mean(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.mean(axis, skipna, level, numeric_only, **kwargs)
        return ans

    @copy_doc(pd.Series.skew)
    def skew(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.skew(axis, skipna, level, numeric_only, **kwargs)
        return ans

    @copy_doc(pd.Series.kurt)
    def kurt(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.kurt(axis, skipna, level, numeric_only, **kwargs)
        return ans

    @copy_doc(pd.Series.median)
    def median(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.median(axis, skipna, level, numeric_only, **kwargs)
        return ans

    @copy_doc(pd.Series.max)
    def max(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.max(axis, skipna, level, numeric_only, **kwargs)
        return ans

    @copy_doc(pd.Series.min)
    def min(
        self,
        axis: Optional[Axis] = no_default,
        skipna: bool = True,
        level: Optional[Level] = None,
        numeric_only: Optional[bool] = None,
        **kwargs,
    ) -> Union[Scalar, pd.Series]:
        ans = self.series.min(axis, skipna, level, numeric_only, **kwargs)
        return ans

    @copy_doc(pd.Series.add)
    def add(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.add(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.radd)
    def radd(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.radd(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.mul)
    def mul(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.mul(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.truediv)
    def truediv(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.truediv(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.floordiv)
    def floordiv(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.floordiv(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.mod)
    def mod(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.mod(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.pow)
    def pow(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.pow(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.rmul)
    def rmul(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rmul(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.rsub)
    def rsub(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rsub(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.rtruediv)
    def rtruediv(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rtruediv(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.rfloordiv)
    def rfloordiv(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rfloordiv(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.rpow)
    def rpow(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rpow(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.rmod)
    def rmod(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rmod(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.divmod)
    def divmod(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.divmod(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.rdivmod)
    def rdivmod(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.rdivmod(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.eq)
    def eq(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.eq(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.ne)
    def ne(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.ne(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.lt)
    def lt(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.lt(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.gt)
    def gt(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.gt(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.le)
    def le(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.le(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.ge)
    def ge(
        self,
        other: Union[Scalar, pd.Series],
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        ans = self.series.ge(other, level, fill_value, axis)
        return ProxyObject(ans)

    @copy_doc(pd.Series.sub)
    def sub(
        self,
        other: "SeriesRemote",
        level: Optional[Level] = None,
        fill_value: Optional[Scalar] = None,
        axis: Axis = 0,
    ) -> Type[ProxyObject]:
        if isinstance(other, SeriesRemote):
            other = other.series
        ans = self.series.sub(other, level, fill_value, axis)
        ans = SeriesRemote(d=ans)
        return ProxyObject(ans)

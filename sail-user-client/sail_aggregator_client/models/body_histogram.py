from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyHistogram")


@attr.s(auto_attribs=True)
class BodyHistogram:
    """
    Attributes:
        series_1_id (str): The identifier of the Series
        bin_count (int): How many bins to sort the Series into.
    """

    series_1_id: str
    bin_count: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        series_1_id = self.series_1_id
        bin_count = self.bin_count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "series_1_id": series_1_id,
                "bin_count": bin_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        series_1_id = d.pop("series_1_id")

        bin_count = d.pop("bin_count")

        body_histogram = cls(
            series_1_id=series_1_id,
            bin_count=bin_count,
        )

        body_histogram.additional_properties = d
        return body_histogram

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

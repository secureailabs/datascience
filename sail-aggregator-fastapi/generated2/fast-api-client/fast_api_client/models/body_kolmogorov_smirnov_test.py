from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyKolmogorovSmirnovTest")


@attr.s(auto_attribs=True)
class BodyKolmogorovSmirnovTest:
    """
    Attributes:
        series_1_id (str): the identifier of the Series to be computed
        type_distribution (str): Type of distribution of Series. May be 'normal' or 'normal unit'
    """

    series_1_id: str
    type_distribution: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        series_1_id = self.series_1_id
        type_distribution = self.type_distribution

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "series_1_id": series_1_id,
                "type_distribution": type_distribution,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        series_1_id = d.pop("series_1_id")

        type_distribution = d.pop("type_distribution")

        body_kolmogorov_smirnov_test = cls(
            series_1_id=series_1_id,
            type_distribution=type_distribution,
        )

        body_kolmogorov_smirnov_test.additional_properties = d
        return body_kolmogorov_smirnov_test

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

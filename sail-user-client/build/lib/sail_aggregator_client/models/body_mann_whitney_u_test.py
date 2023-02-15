from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyMannWhitneyUTest")


@attr.s(auto_attribs=True)
class BodyMannWhitneyUTest:
    """
    Attributes:
        series_1_id (str): The identifer of Series 1.
        series_2_id (str): The identifier of Series 2.
        alternative (str): Alternative must be of 'less', 'two-sided' or 'greater'
    """

    series_1_id: str
    series_2_id: str
    alternative: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        series_1_id = self.series_1_id
        series_2_id = self.series_2_id
        alternative = self.alternative

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "series_1_id": series_1_id,
                "series_2_id": series_2_id,
                "alternative": alternative,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        series_1_id = d.pop("series_1_id")

        series_2_id = d.pop("series_2_id")

        alternative = d.pop("alternative")

        body_mann_whitney_u_test = cls(
            series_1_id=series_1_id,
            series_2_id=series_2_id,
            alternative=alternative,
        )

        body_mann_whitney_u_test.additional_properties = d
        return body_mann_whitney_u_test

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
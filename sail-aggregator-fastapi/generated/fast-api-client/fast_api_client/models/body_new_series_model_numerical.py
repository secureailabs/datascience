from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyNewSeriesModelNumerical")


@attr.s(auto_attribs=True)
class BodyNewSeriesModelNumerical:
    """
    Attributes:
        series_name (str): name of the series
        measurement_source_name (str): Source featuree of the series.
        type_agregator (str): Method by which source of data is to be aggregated
        unit (str): The unit type of the series model
    """

    series_name: str
    measurement_source_name: str
    type_agregator: str
    unit: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        series_name = self.series_name
        measurement_source_name = self.measurement_source_name
        type_agregator = self.type_agregator
        unit = self.unit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "series_name": series_name,
                "measurement_source_name": measurement_source_name,
                "type_agregator": type_agregator,
                "unit": unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        series_name = d.pop("series_name")

        measurement_source_name = d.pop("measurement_source_name")

        type_agregator = d.pop("type_agregator")

        unit = d.pop("unit")

        body_new_series_model_numerical = cls(
            series_name=series_name,
            measurement_source_name=measurement_source_name,
            type_agregator=type_agregator,
            unit=unit,
        )

        body_new_series_model_numerical.additional_properties = d
        return body_new_series_model_numerical

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

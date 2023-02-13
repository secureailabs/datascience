from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyDataframeModelAddNewSeriesModel")


@attr.s(auto_attribs=True)
class BodyDataframeModelAddNewSeriesModel:
    """
    Attributes:
        data_model_id (str): Reference to the data model being added to.
        series_name (str): Name of the new series model to be added.
        measurement_source_name (str): The feature to aggregate.
        type_agregator (str): Method by which source of data is to be aggregated for new series model
        unit (str): The unit of measurement of the new series to be added.
    """

    data_model_id: str
    series_name: str
    measurement_source_name: str
    type_agregator: str
    unit: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_model_id = self.data_model_id
        series_name = self.series_name
        measurement_source_name = self.measurement_source_name
        type_agregator = self.type_agregator
        unit = self.unit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_model_id": data_model_id,
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
        data_model_id = d.pop("data_model_id")

        series_name = d.pop("series_name")

        measurement_source_name = d.pop("measurement_source_name")

        type_agregator = d.pop("type_agregator")

        unit = d.pop("unit")

        body_dataframe_model_add_new_series_model = cls(
            data_model_id=data_model_id,
            series_name=series_name,
            measurement_source_name=measurement_source_name,
            type_agregator=type_agregator,
            unit=unit,
        )

        body_dataframe_model_add_new_series_model.additional_properties = d
        return body_dataframe_model_add_new_series_model

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

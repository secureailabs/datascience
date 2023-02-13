from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyTabularModelAddDataframeModel")


@attr.s(auto_attribs=True)
class BodyTabularModelAddDataframeModel:
    """
    Attributes:
        data_model_tabular_id (str): The reference to the Tabular Dataframe model being added to.
        data_model_dataframe_id (str): The reference to the Dataframe model being added to the Tabular Dataframe.
    """

    data_model_tabular_id: str
    data_model_dataframe_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_model_tabular_id = self.data_model_tabular_id
        data_model_dataframe_id = self.data_model_dataframe_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_model_tabular_id": data_model_tabular_id,
                "data_model_dataframe_id": data_model_dataframe_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data_model_tabular_id = d.pop("data_model_tabular_id")

        data_model_dataframe_id = d.pop("data_model_dataframe_id")

        body_tabular_model_add_dataframe_model = cls(
            data_model_tabular_id=data_model_tabular_id,
            data_model_dataframe_id=data_model_dataframe_id,
        )

        body_tabular_model_add_dataframe_model.additional_properties = d
        return body_tabular_model_add_dataframe_model

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

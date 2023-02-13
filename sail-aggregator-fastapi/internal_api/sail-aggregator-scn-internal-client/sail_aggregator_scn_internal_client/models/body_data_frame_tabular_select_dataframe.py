from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyDataFrameTabularSelectDataframe")


@attr.s(auto_attribs=True)
class BodyDataFrameTabularSelectDataframe:
    """
    Attributes:
        data_frame_tabular_id (str): The identifier of the dataframe being queried.
        data_frame_name (str): The name of the dataframe being pulled from the tabular dataframe.
    """

    data_frame_tabular_id: str
    data_frame_name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_frame_tabular_id = self.data_frame_tabular_id
        data_frame_name = self.data_frame_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_frame_tabular_id": data_frame_tabular_id,
                "data_frame_name": data_frame_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data_frame_tabular_id = d.pop("data_frame_tabular_id")

        data_frame_name = d.pop("data_frame_name")

        body_data_frame_tabular_select_dataframe = cls(
            data_frame_tabular_id=data_frame_tabular_id,
            data_frame_name=data_frame_name,
        )

        body_data_frame_tabular_select_dataframe.additional_properties = d
        return body_data_frame_tabular_select_dataframe

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

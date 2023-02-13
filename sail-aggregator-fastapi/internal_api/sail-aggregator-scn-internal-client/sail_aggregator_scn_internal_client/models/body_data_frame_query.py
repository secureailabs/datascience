from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyDataFrameQuery")


@attr.s(auto_attribs=True)
class BodyDataFrameQuery:
    """
    Attributes:
        data_frame_id (str): The identifier of the dataframe to be queried.
        query_str (str): The string to be queried.
    """

    data_frame_id: str
    query_str: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data_frame_id = self.data_frame_id
        query_str = self.query_str

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data_frame_id": data_frame_id,
                "query_str": query_str,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data_frame_id = d.pop("data_frame_id")

        query_str = d.pop("query_str")

        body_data_frame_query = cls(
            data_frame_id=data_frame_id,
            query_str=query_str,
        )

        body_data_frame_query.additional_properties = d
        return body_data_frame_query

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

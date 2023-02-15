from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="DataFederation")


@attr.s(auto_attribs=True)
class DataFederation:
    """
    Attributes:
        list_dataset_id (List[str]):
    """

    list_dataset_id: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        list_dataset_id = self.list_dataset_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "list_dataset_id": list_dataset_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        list_dataset_id = cast(List[str], d.pop("list_dataset_id"))

        data_federation = cls(
            list_dataset_id=list_dataset_id,
        )

        data_federation.additional_properties = d
        return data_federation

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

from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyReadDatasetTabularFromLongitudinal")


@attr.s(auto_attribs=True)
class BodyReadDatasetTabularFromLongitudinal:
    """
    Attributes:
        longitudinal_id (str): The identifier of the Longitudinal Dataset to be added from.
        dataset_federation_id (str): The identifier of the dataset federation
        dataset_federation_name (str): The name of the federation being worked with.
        data_model_tabular_id (str): the identifier of the data model being used to query from the longitudinal dataset.
    """

    longitudinal_id: str
    dataset_federation_id: str
    dataset_federation_name: str
    data_model_tabular_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        longitudinal_id = self.longitudinal_id
        dataset_federation_id = self.dataset_federation_id
        dataset_federation_name = self.dataset_federation_name
        data_model_tabular_id = self.data_model_tabular_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "longitudinal_id": longitudinal_id,
                "dataset_federation_id": dataset_federation_id,
                "dataset_federation_name": dataset_federation_name,
                "data_model_tabular_id": data_model_tabular_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        longitudinal_id = d.pop("longitudinal_id")

        dataset_federation_id = d.pop("dataset_federation_id")

        dataset_federation_name = d.pop("dataset_federation_name")

        data_model_tabular_id = d.pop("data_model_tabular_id")

        body_read_dataset_tabular_from_longitudinal = cls(
            longitudinal_id=longitudinal_id,
            dataset_federation_id=dataset_federation_id,
            dataset_federation_name=dataset_federation_name,
            data_model_tabular_id=data_model_tabular_id,
        )

        body_read_dataset_tabular_from_longitudinal.additional_properties = d
        return body_read_dataset_tabular_from_longitudinal

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

from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="BodyDatasetTabularFhirv1")


@attr.s(auto_attribs=True)
class BodyDatasetTabularFhirv1:
    """
    Attributes:
        dataset_federation_id (str): The identifier of the data federation
        dataset_federation_name (str): the name of the data federation
        data_model_tabular_id (str): The identifier of the tabular dataframe modle being used to pull data from the
            fhirv1 source.
    """

    dataset_federation_id: str
    dataset_federation_name: str
    data_model_tabular_id: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dataset_federation_id = self.dataset_federation_id
        dataset_federation_name = self.dataset_federation_name
        data_model_tabular_id = self.data_model_tabular_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset_federation_id": dataset_federation_id,
                "dataset_federation_name": dataset_federation_name,
                "data_model_tabular_id": data_model_tabular_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dataset_federation_id = d.pop("dataset_federation_id")

        dataset_federation_name = d.pop("dataset_federation_name")

        data_model_tabular_id = d.pop("data_model_tabular_id")

        body_dataset_tabular_fhirv_1 = cls(
            dataset_federation_id=dataset_federation_id,
            dataset_federation_name=dataset_federation_name,
            data_model_tabular_id=data_model_tabular_id,
        )

        body_dataset_tabular_fhirv_1.additional_properties = d
        return body_dataset_tabular_fhirv_1

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

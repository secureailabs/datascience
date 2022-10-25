import json

from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions_orchestrator.reference_dataset_tabular import ReferenceDatasetTabular
from sail_safe_functions_orchestrator.service_reference import ServiceReference


class ConvertToDatasetTabularPrecompute:
    def run(
        reference_dataset_logitudinal: ReferenceDatasetLongitudinal,
        dataset_federation_id: str,
        dataset_federation_name: str,
        dataset_id: str,
        dataset_name: str,
        data_model_tabular: DataModelTabular,
    ) -> ReferenceDatasetTabular:
        dataset_logitudinal = ServiceReference.get_instance().reference_to_dataset_longitudinal(
            reference_dataset_logitudinal
        )
        dataset_tabular = dataset_logitudinal.convert_to_dataset_tabular(
            dataset_federation_id, dataset_federation_name, dataset_id, dataset_name, data_model_tabular
        )
        return ServiceReference.get_instance().dataset_tabular_to_reference(dataset_tabular)
